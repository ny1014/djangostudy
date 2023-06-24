from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from platformdirs import user_cache_dir
from .models import Room,User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1','password2']

  
class RoomForm(ModelForm):
    class Meta:
        model = Room
        #get all room fileds
        fields ='__all__'
        exclude = ['host','participants']
        # fields = ['name','body']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name','username','email','bio']
      
     