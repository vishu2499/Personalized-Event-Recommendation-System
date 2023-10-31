from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.contrib.auth.models import User
from user_app.forms import UserForm
from .models import UserProfile
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def createUser(request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        print("Inside the post request")

        print(form)

        if form.is_valid():

            # getting information from the form.
            firstname = form.cleaned_data["firstname"]
            lastname = form.cleaned_data["lastname"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            phone_number = form.cleaned_data["phone_number"]
            # age = form.cleaned_data["age"]
            # birth_date = form.cleaned_data["birth_date"]


            # creating the user model
            cu_user = User.objects.create_user(username=email,email=email)
            cu_user.set_password(password)
            cu_user.first_name = firstname
            cu_user.last_name = lastname
            cu_user.save()

            # saving other details about the user.
            user_profile = UserProfile(user=cu_user,phone_number=phone_number)
            user_profile.save()

            print("-------CUSTOM PRINT STATEMENT--------")
            print("Data has been inserted into the database")

            return redirect('/user/login',{})
        
        else:
            print("form is invalid")

    else:
        form = UserForm
    
    return render(request,'users/signup.html',{'form':form})

def loginUser(request):

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('event_list')
        else:
            return HttpResponse("<h1>Invalid Credentials</h1>")
    
    return render(request,'users/login.html',{})

@login_required
def logoutUser(request):
    logout(request)
    return redirect('event_list')