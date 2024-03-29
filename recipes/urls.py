from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^view/(?P<recipe_name>.+)/$', views.view, name='view'),
    url(r'^ingredients/(?P<recipe_name>.+)/$', views.ingredients, name='ingredients')
]
