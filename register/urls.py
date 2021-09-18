from django.urls import path
from . import views


app_name = "register"
urlpatterns = [
    path('', views.info, name='info'),
    path('index', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view , name = 'logout'),
    path('upload', views.upload , name = 'upload'),
    path('admin_index', views.index , name = "admin_index"),
    path('<subject_id>',views.subject_info, name = 'subjectinfo'),
    path('<subject_id>/enroll' ,views.enroll , name = 'enroll'),
    path('<subject_id>/unenroll' ,views.unenroll , name = 'unenroll'),
    path('<subject_id>/admin_subject_info',views.admin_subject_info, name = 'admin_subject_info'),
]
    