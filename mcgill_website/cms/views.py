from cms.models import Page
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
import os

args_404 = {'title': '404 Not Found', 'content':'The page requested does not exist. La page demandée n\'existe pas.', 'custom_js_css': ''}

#l2_page, l3_page: model reference ; language: string 'en' or 'fr'
def make_navbar_content(l2_page,l3_page,language):
    page_name_attr = 'page_name_'+language
    page_title_attr = 'page_title_'+language
    page_content_attr = 'page_content_'+language
    custom_js_css_attr = 'custom_js_css_'+language

    l2_to_add = Page.objects.get(page_name_en="home").children.all()
    navbar_content = []
    for i in l2_to_add:
        l2_at_current = l2_page==i
        l3_pages = []
        for j in i.children.all():
            l3_at_current = l3_page==j
            l3_pages.append({'l3_name':getattr(j,page_title_attr),'l3_link':'/'+language+'/'+getattr(i,page_name_attr)+'/'+getattr(j,page_name_attr),'is_current':l3_at_current})
        navbar_content.append({'l2_name':getattr(i,page_title_attr),'l2_link':'/'+language+'/'+getattr(i,page_name_attr),'is_current':l2_at_current,'l3_items':l3_pages})
    return navbar_content

args_404 = {'title': '404 Not Found', 'content':'The page requested does not exist. La page demandée n\'existe pas.', 'custom_js_css': '','current_language':'en','other_language_link':'/'}

def render_404(request):
    return render(request,'base.html',{**args_404,'navbar_content':make_navbar_content(None,None,'en')})

# Create your views here.
def cms_view(request):
    path_list = os.path.normpath(request.path).split(os.path.sep) #parse path into a list
    language = path_list[1] #need to add something to handle the situation where a user types the path / without en or fr
    path_list = path_list[2:] 
    
    if request.path=='/': #if the user only typed the domain without following it with /en or /fr, then load the English home page
        language = 'en'
        path_list = []

    if language!='en' and language!='fr':
        return render_404(request)

    other_language = 'en' if language=='fr' else 'fr'
    page_name_attr = 'page_name_'+language
    page_title_attr = 'page_title_'+language
    page_content_attr = 'page_content_'+language
    custom_js_css_attr = 'custom_js_css_'+language
    #Find the page specified by the path by traversing the database in a tree-like manner starting from home
    #We start from the home page. The home page must have page_name_en = 'home'
    cur = Page.objects.filter(page_name_en='home')[0]
    not_found = False
    #For each next level specified in the path, match with one of the children of the current node. not_found becomes true because such a node is not found
    l2_page = None
    l3_page = None
    level = 2
    other_language_path = '/'+ other_language
    for dir in path_list:
        if language=="en":
            temp = cur.children.filter(page_name_en=dir)
        elif language=="fr":
            temp = cur.children.filter(page_name_fr=dir)

        if len(temp)> 0:
            cur = temp[0]
            other_language_path += '/'+ getattr(cur,'page_name_'+other_language)
            if level == 2:
                l2_page = cur
            if level == 3:
                l3_page = cur
            level = level + 1    

        else:
            not_found = True
            break

    navbar_content = make_navbar_content(l2_page,l3_page,language)
    if not_found:
        return render_404(request)
    else:
        args = {'title': getattr(cur,page_title_attr),
        'content': getattr(cur,page_content_attr),
        'custom_js_css': getattr(cur,custom_js_css_attr),
        'current_language': language,
        'other_language_link': other_language_path,
        'navbar_content': navbar_content
        }
        return render(request,'base.html',args)