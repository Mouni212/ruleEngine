from . import views
from django.urls import path

urlpatterns = [
    path('create_rules', views.create_rule, name='create_rule'),
    path('get_rule', views.get_rule, name='get_rule'),
    path('delete_rule', views.delete_rule, name='delete_rule')
]
