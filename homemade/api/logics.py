from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.conf import settings
from django.forms.models import model_to_dict
import models
import collections
import simplejson as json
import datetime

def _myModelToDict(obj):
    d = model_to_dict(obj)
    for k,v in d.iteritems():
        if isinstance(v, datetime.datetime) or isinstance(v, datetime.date):
            d[k] = v.strftime('%Y-%m-%d')
    return d

def _getUserList():
    return models.User.objects.all()

def _getFoodList():
    return models.Food.objects.all()

def _getUserFoodDict():
    dic = collections.defaultdict(list)
    for food in _getFoodList():
        dic[food.user_id].append(_myModelToDict(food))
    return dic

def _getPagerQueryset(queryset, page):
    paginator = Paginator(queryset, settings.SINGLE_PAGE_NUM)
    print paginator.num_pages
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        object_list = paginator.page(page)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
        page = paginator.num_pages
    return object_list, page, paginator.num_pages

def _getListFinalDict(page, pageNum):
    return {
        'array' : [],
        'page_count' : pageNum,
        'page_index' : page,
        'page_items' : settings.SINGLE_PAGE_NUM,
    }

def getCookUserList(page):
    cookUsers = _getUserList().exclude(kitchen=None)
    object_list, page, max_page = _getPagerQueryset(cookUsers, page)
    final_dict = _getListFinalDict(page, max_page)
    userFoodDict = _getUserFoodDict()
    
    for cooker in object_list:
        itemDict = _myModelToDict(cooker)
        itemDict["food"] = userFoodDict.get(cooker.pk)
        final_dict['array'].append(itemDict)

    return final_dict

def _getTagList():
    return models.Tag.objects.all()

def getTagList():
    return _getTagList()

def getFoodListByTag(tag, page):
    objs = models.FoodTag.objects.filter(tag_id=tag)
    object_list, page, max_page = _getPagerQueryset(objs, page)
    final_dict = _getListFinalDict(page, max_page)
    for obj in object_list:
        final_dict.update(_myModelToDict(obj.tag))
        final_dict['array'].append(_myModelToDict(obj.food))
    return final_dict    