from cms.models import Page
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
import os

args_404 = {'title': '404 Not Found', 'content':'The page requested does not exist. La page demandée n\'existe pas.', 'custom_js_css': ''}

# Create your views here.
def cms_view(request):
    path_list = os.path.normpath(request.path).split(os.path.sep) #parse path into a list
    language = path_list[1] #need to add something to handle the situation where a user types the path / without en or fr
    path_list = path_list[2:] 

    if request.path=='/': #if the user only typed the domain without following it with /en or /fr, then load the English home page
        language = 'en'
        path_list = []

    if language!='en' and language!='fr':
        return render(request,'base.html',args_404)

    #Find the page specified by the path by traversing the database in a tree-like manner starting from home
    #We start from the home page. The home page must have page_name_en = 'home'
    cur = Page.objects.filter(page_name_en='home')[0]
    not_found = False
    #For each next level specified in the path, match with one of the children of the current node. not_found becomes true because such a node is not found
    for dir in path_list:
        if language=="en":
            temp = cur.children.filter(page_name_en=dir)
        elif language=="fr":
            temp = cur.children.filter(page_name_fr=dir)

        if len(temp)> 0:
            cur = temp[0]
        else:
            not_found = True

    if not_found:
        return render(request,'base.html',args_404)
    else:
        if language=='en':
            args = {'title': cur.page_title_en, 'content': cur.page_content_en, 'custom_js_css': cur.custom_js_css_en}
        else: #french
            args = {'title': cur.page_title_fr, 'content': cur.page_content_fr, 'custom_js_css': cur.custom_js_css_fr}

        return render(request,'base.html',args)