from django import forms  
from organizer.models import Organizer  
from events.models import Event_category_model
class OrgForm(forms.ModelForm):  
    class Meta:  
        model = Organizer  
        fields = "__all__"  