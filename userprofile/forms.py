from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class UserRegisterForm(UserCreationForm):
    # add email as defail user create form
    email = forms.EmailField(label = "Email")

    class Meta:
        model = User
        fields = ('username', 'email',)


# User profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')
