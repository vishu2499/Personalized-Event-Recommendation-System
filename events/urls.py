from django.urls import path

from . import views

from events.views import EventsListView,EventDetailView

urlpatterns = [
    # path('', views.index, name='index'),
    path('',EventsListView.as_view(),name='event_list'),
    path('<int:category_pk>',EventsListView.as_view(),name='event_list'),
    path('<slug:search_q>',EventsListView.as_view(),name='event_list'),
    path('<slug:pk>/',EventDetailView.as_view(),name='event_detail'),
    path('<slug:location>',EventsListView.as_view(),name='event_list')
]
