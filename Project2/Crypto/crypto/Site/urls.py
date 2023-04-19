from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit', views.submit, name='submit'),
    path('badcredentials', views.badcredentials, name='badcreds'),
    path('home', views.home, name='home'),
    path('createuser', views.createuser, name='createuser'),
    path('submitcreate', views.submitcreate, name='submitcreate'),
    path('upload', views.upload, name='upload'),
    path('add', views.add, name='add'),
    path('remove', views.remove, name='remove'),
    path('create', views.create, name='create'),
    path('delete', views.delete, name='delete'),
    path('deletefile/<str:group>/<str:fileDelete>', views.deletefile, name='fileDelete'),
    path('files', views.files, name='files'),
    path('change', views.change, name='change'),
    path('exit', views.exit, name='exit'),
    path('download/<str:group>/<str:fileDownload>', views.download, name='download')
]