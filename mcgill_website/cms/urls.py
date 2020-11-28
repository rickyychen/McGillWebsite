from django.conf.urls import url, include
from django.urls import path, re_path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('widgets/calendar/',views.calendar_widget),
    path('widgets/job_posting/', views.job_posting_widget),
    path('cms_management_api/delete_page/<slug:page_id>/',views.cms_editor_client_delete_page),
    path('cms_management_api/create_page/',views.cms_editor_create_page),
    path('cms_management_api/edit_page/<slug:page_id>/',views.cms_editor_client_edit_page),
    path('cms_management_api/get_tree/',views.cms_editor_client_get_tree),
    re_path(r'^cms_management/editor[|/]',views.cms_editor_view),
    #path('cms_management/editor',RedirectView.as_view(url = '/cms_management/editor/')),
    re_path(r'cms_management[|/]',RedirectView.as_view(url = '/cms_management/editor/')),
    path('cms_management',RedirectView.as_view(url = '/cms_management/')),
    url(r'.*',views.cms_view)

]
