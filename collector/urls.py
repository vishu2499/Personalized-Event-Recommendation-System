from django.urls import path

from . import views


urlpatterns = [
    # path('', views.index, name='index'),
    path('put_evidence/',views.CollectBrowsingData.as_view(),name='test_for_collector'),
    
]