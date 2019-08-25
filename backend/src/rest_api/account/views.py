from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserSignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

# From line 1 to 11 – we import the classes that we are going to use create our logic. 
# This include our signup form and token generator.

# Line 38 – we create our signup method.

# Line 43 – we make the user in active so that they cannot login to our application.

# Line 45 – we get the current site from the request.

# Line 46 – we create the subject of our email.

# Line 47 – we create a message of our email. One thing to note is that we are using a activate_account.html that we will create.

# Line 48 to 51 – we pass the content to our template, this include token, user, domain, an uid.

# Line 53 – we get the user email from our form.

# Line 54 – we create email instance and pass subject, message and who we are sending email to.

# Line 55 – we send the email.

# Line 56 – we return a http response asking the user to complete registration by checking their email.

# Line 58 – if the request was not a post, we return the form user to fill.

def usersignup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST, request=request)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
    else:
        form = UserSignUpForm()

    return render(request, 'signup.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64)).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activate successfully')
    else:
        return HttpResponse('Activation link is invalid!')