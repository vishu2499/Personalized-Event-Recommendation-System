from django.urls import path

from . import views
from user_app.views import createUser,loginUser, logoutUser

urlpatterns = [
   path('create/',createUser,name='create_user'),
   path('login/',loginUser,name='login_user'),
   path('logout/',logoutUser,name='logout_user'),
]



