from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView, DetailView
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.core import serializers
from django.conf import settings

import simplejson as json
import logging
import traceback

log = logging.getLogger('main')

def crossDomainResponse(response):
    """
        for cross domain ajax post
        not used any more when using corsheaders
    """
    if settings.DEBUG:
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    return response

def buildResponseJson(returnCode, entry = ''):
    data = {
        'ret': returnCode[0],
        'reason': returnCode[1] % entry
    }
    return data

class jsonResponseMixin(object):
    
    def render_to_json_response(self, context, **response_kwargs):
        """
            Returns a JSON response, transforming 'context' to make the payload.
        """
        return_data = self.get_json_data(context)
        return HttpResponse(return_data, content_type='application/json')

class ajaxPostFormRequest(object):
    def json_response(self, jsonObj, returnCode, entry='', status=200):
        jsonObj.update(buildResponseJson(returnCode, entry))
        return JsonResponse(jsonObj, status=status)

    def form_invalid(self, form):
        log.info("form invalid: %s" % form.errors)
        response = super(ajaxPostFormRequest, self).form_invalid(form)
        return self.json_response(form.errors, error_code.MISSING_PARAMS_ERROR)

    def form_valid(self, form):
        if self.request.user.is_authenticated():
            email = self.request.user.email
        else:
            email = 'dev@gmail.com'
            
        try:
            response = super(ajaxPostFormRequest, self).form_valid(form)
            data = {'pk': self.object.pk}
            log.info("form valid -> Success! %s. Done by: %s" % 
                (
                    json.dumps(form.cleaned_data, indent=4), 
                    email
                ))
            return self.json_response(data, error_code.SUCCESS)
        except IntegrityError as e:
            log.info("form valid -> IntegrityError: %s" % traceback.print_exc())
            return self.json_response({}, error_code.INTEGRITY_ERROR)
        except Exception as e:
            log.info("form valid -> %s" % traceback.print_exc())
            return self.json_response({}, error_code.UNKNOWN_ERROR)

class ajaxableResponseMixin(ajaxPostFormRequest):
    def get_form_kwargs(self):
        """
            Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(ajaxableResponseMixin, self).get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        try:
            data = json.loads(self.request.body)
            form_data = {}
            for key, value in data.iteritems():
                if type(value) is list or type(value) is dict:
                    form_data[key] = json.dumps(value)
                else:
                    form_data[key] = value
        except Exception as e:
            form_data = {}
            log = logging.getLogger('main')
            log.info("get_form_kwargs: %s" % traceback.print_exc())
        kwargs.update({'data': form_data})
        return kwargs

class ListBaseView(jsonResponseMixin, BaseListView):
    def get_json_data(self, context):
        result = self.get_queryset()

        paginator = Paginator(result, settings.SINGLE_PAGE_NUM)

        # check whether for dropdown list, display all
        pager = self.request.GET.get('list', '')
        if pager == 'all':
            return serializers.serialize('json', result)

        # for management page, display by page number
        page = int(self.request.GET.get('page','1'))

        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            object_list = paginator.page(page)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
            page = paginator.num_pages

        obj_list_str = serializers.serialize('json', object_list)
        obj_list = json.loads(obj_list_str)

        final_json = {}
        final_json['array'] = obj_list
        if len(obj_list) > 0:
            final_json['page_count'] = paginator.num_pages
            final_json['page_index'] = page
            final_json['page_items'] = settings.SINGLE_PAGE_NUM
        return json.dumps(final_json)

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)
