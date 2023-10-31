from . import views
from django.urls import path
from organizer import views  
urlpatterns = [     
    path('new', views.org,name='new-organizer'),  
    path('show',views.show),  
    path('edit/<int:id>', views.edit),  
    path('update/<int:id>', views.update),  
    path('delete/<int:id>', views.destroy), 
]