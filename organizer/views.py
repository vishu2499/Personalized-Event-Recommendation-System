from django.shortcuts import render, redirect  
from organizer.forms import OrgForm  
from organizer.models import Organizer  
from events.models import Event_category_model
# Create your views here.  
def org(request):  
    if request.method == "POST":  
        form = OrgForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/organizer/show')  
            except:  
                pass  
    else:  
        form = OrgForm()  
    return render(request,'organizer/index.html',{'form':form})  
def show(request):  
    organizer = Organizer.objects.all()  
    return render(request,"organizer/show.html",{'organizer':organizer})  
def edit(request, id):  
    organizer = Organizer.objects.get(id=id)  
    return render(request,'organizer/edit.html', {'organizer':organizer})  
def update(request, id):  
    organizer = Organizer.objects.get(id=id)  
    form = OrgForm(request.POST, instance = organizer)  
    if form.is_valid():  
        form.save()  
        return redirect("/organizer/show")  
    return render(request, 'organizer/edit.html', {'organizer': organizer})  
def destroy(request, id):  
    organizer = Organizer.objects.get(id=id)  
    organizer.delete()  
    return redirect("/organizer/show")  