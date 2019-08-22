from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token

# Create your views here.

class Signup(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'signup.html', {"form": form})
    
    def post(self, request):
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                # Create an inactive user with no password:
                user = form.save(commit = False)
                user.is_active = False
                user.set_unusable_password()
                user.save()

                # Send an email to the user with the token:
                mail_subject = 'Activate your Account'
                current_site = get_current_site(request)
                uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
                token = account_activation_token.make_token(user)
                activation_link = "{0}/?uid={1}&token{2}".format(current_site, uid, token)
                message = "Hello {0},\n {1}".format(user.username, activation_link)
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return HttpResponse('Please confirm your email address to complete the registration')
        else:
            form = SignupForm()
            return render(request, 'signup.html', {'form': form})


User = get_user_model()

class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            # activate user and login:
            user.is_active = True
            user.save()
            login(request, user)

            form = PasswordChangeForm(request.user)
            return render(request, 'activation.html', {'form': form})

        else:
            return render(request, 'activation.html', {'form': form })

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) # Important, to update the session with the new password
            return HttpResponse('Password changed successfully')