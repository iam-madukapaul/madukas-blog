from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm, CreateUserForm, SetPasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from cms_app.models import Category


# Create your views here.
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Email confirmation successful. Login!')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('index')

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account'
    message = render_to_string('activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Hello {user}, please go to your email {to_email} inbox and click on the\
                        received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you entered the correct email.')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        categories = Category.objects.all()
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST) 
            if form.is_valid():
                user =form.save(commit=False)
                user.is_active = False
                user.save()
                activateEmail(request, user, form.cleaned_data.get('email'))

                subject = 'Welcome to Maduka"s blog'
                email_template_name = 'welcome_message.html'
                parameters = {
                    'email': user.email,
                    'username': user.username,
                    'domain': get_current_site(request).domain,
                    'site_name': 'Madukasblog',
                    'protocol': 'https' if request.is_secure() else 'http'
                }
                email = render_to_string(email_template_name, parameters)
                try:
                    send_mail(subject, email, '', [user.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid Header')
                return redirect('login')
                
        context = {
            'categories':categories,
            'form':form
        }
        return render(request, 'register_user.html', context)

def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        categories = Category.objects.all()
        form = AuthenticationForm()
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Login successful.')
                    return redirect('index')
        context = {'categories':categories, 'form':form}
        return render(request, 'login_user.html', context)

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('index')

def user_profile(request, pk):
    profile = UserProfile.objects.get(pk=pk)
    context = {
        'profile':profile,
    }
    return render(request, 'user_profile.html', context)

@login_required(login_url='login')
def user_account(request):
    account = request.user.userprofile
    context = {
        'account':account,
    }
    return render(request, 'user_account.html', context)

@login_required(login_url='login')
def update_user_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('account')
        else:
            messages.info(request, 'Something went wrong!')
            return redirect('account')
    else:
        form = UserProfileForm(instance=profile)
    context = {
        'form':form
    }
    return render(request, 'update_user_profile.html', context)

@login_required(login_url='login')
def delete_user_profile(request):
    profile = request.user.userprofile
    profile.delete()
    
    return redirect('index')

def password_reset_custom(request):
    if request.method == 'POST':
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            data = password_form.cleaned_data['email']
            user_email = User.objects.filter(Q(email=data))
            if user_email.exists():
                for user in user_email:
                    subject = 'Password Reset'
                    email_template_name = 'password_message.txt'
                    parameters = {
                        'email': user.email,
                        'username': user.username,
                        'domain': get_current_site(request).domain,
                        'site_name': 'Madukasblog',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https' if request.is_secure() else 'http'
                    }
                    email = render_to_string(email_template_name, parameters)
                    try:
                        send_mail(subject, email, '', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid Header')
                    return redirect('password_reset_done')
    else:
        password_form = PasswordResetForm()
    context = {
        'password_form': password_form,
    }
    return render(request, 'reset_password.html', context)


@login_required(login_url='login')
def change_password(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been changed.')
            return redirect('login')
    form = SetPasswordForm(user)
    context = {
        'form':form
    }
    return render(request, 'change_password.html', context)
   