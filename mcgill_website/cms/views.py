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
    page_name_attr = 'page_name_'+language
    page_title_attr = 'page_title_'+language
    page_content_attr = 'page_content_'+language
    custom_js_css_attr = 'custom_js_css'+language
    if request.path=='/': #if the user only typed the domain without following it with /en or /fr, then load the English home page
        language = 'en'
        path_list = []

    if language!='en' and language!='fr':
        return render(request,'base.html',args_404)

    #Find the page specified by the path by traversing the database in a tree-like manner starting from home
    #We start from the home page. The home page must have page_name_en = 'home'
    navbar_content = []
    cur = Page.objects.filter(page_name_en='home')[0]
    not_found = False
    #For each next level specified in the path, match with one of the children of the current node. not_found becomes true because such a node is not found
    depth = 1
    for dir in path_list:
        if language=="en":
            temp = cur.children.filter(page_name_en=dir)
        elif language=="fr":
            temp = cur.children.filter(page_name_fr=dir)
        
        if len(temp)> 0:
            if depth==1:
                l2_to_add = cur.children.all()
                for i in l2_to_add:
                    l2_at_current = temp[0]==i
                    l3_pages = []
                    for j in i.children.all():
                        l3_at_current = l2_at_current and getattr(j,page_name_attr)==path_list[1]
                        l3_pages.append({'l3_name':getattr(j,page_name_attr),'l3_link':'/en/'+getattr(i,page_name_attr)+'/'+getattr(j,page_name_attr),'is_current':l3_at_current})
                    navbar_content.append({'l2_name':i.page_name_en,'l2_link':'/en/'+i.page_name_en,'is_current':l2_at_current,'l3_items':l3_pages})
            cur = temp[0]
            depth+=1

        else:
            not_found = True

    if not_found:
        return render(request,'base.html',args_404)
    else:
        args = {'title': getattr(cur,page_title_attr),
        'content': getattr(cur,page_content_attr),
        'custom_js_css': getattr(cur,page_content_attr),
        'navbar_content': navbar_content
        }
        return render(request,'base.html',args)