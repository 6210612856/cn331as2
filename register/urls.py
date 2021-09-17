from django.urls import path
from . import views


app_name = "register"
urlpatterns = [
    path('', views.info, name='info'),
    path('index', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view , name = 'logout'),
    path('upload', views.upload , name = 'upload'),
    path('<subject_id>',views.subject_info, name = 'subjectinfo'),
    path('<subject_id>/enroll' ,views.enroll , name = 'enroll'),
    path('<subject_id>/unenroll' ,views.unenroll , name = 'unenroll'),
]
    