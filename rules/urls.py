from . import views
from django.urls import path

urlpatterns = [
    path('createRules/', views.createRule, name='details'),
]