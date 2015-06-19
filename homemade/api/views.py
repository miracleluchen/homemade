from django.shortcuts import render
from homemade.ajaxmixin import ListBaseView, jsonResponseMixin
from django.views.generic import TemplateView
from django.views.generic.list import BaseListView
from django.views.generic.edit import CreateView, BaseFormView, UpdateView, BaseDeleteView
from django.views.generic.detail import BaseDetailView, DetailView
import logics
import simplejson as json

# Create your views here.
class GetUserListView(jsonResponseMixin, TemplateView):
    """
        Index Page, Get Cookers with food list
        Params: page=1
    """
    def get_queryset(self):
        try:
            page = int(self.request.GET.get('page','1'))
        except:
            page = 1

        return logics.getCookUserList(page)

    def get_json_data(self, context):
        result = self.get_queryset()
        return json.dumps(result, use_decimal=True)

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class GetTagListView(ListBaseView):
    """
        Category Page
    """
    def get_queryset(self):
        return logics.getTagList()

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

class GetFoodListByTagView(jsonResponseMixin, TemplateView):
    """
        Food List Page
        Params: page=1
    """
    def get_queryset(self):
        tag = self.kwargs['pk']
        try:
            page = int(self.request.GET.get('page','1'))
        except:
            page = 1
        return logics.getFoodListByTag(tag, page)

    def get_json_data(self, context):
        result = self.get_queryset()
        return json.dumps(result, use_decimal=True)

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)
