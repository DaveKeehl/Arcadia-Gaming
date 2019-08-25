from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email is already used")
        return data

# Line 1 – We import forms from django.

# Line 2 – We import UserCreationForm from django auth.

# Line 3 – We import user model from django auth models.

# Line 5 – We create a UserSignUpForm class where we pass an instance of UserCreationForm.

# Line 6 – We create form field called email with a helper text that is required.

# Line 8 – We create a Meta class for our form.

# Line 9 – We define which model that our form is going to use.

# Line 10 – We define the fields that the user is going to see.