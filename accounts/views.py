# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


# registration code
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect('home')  # Redirect to the home page or another page
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


# email verification
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until email is verified
            user.save()

            # Send verification email
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('accounts/email_verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(subject, message, 'your-email@gmail.com', [user.email])

            return HttpResponse('Please confirm your email address to complete the registration.')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


# activation view
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. You can now log in to your account.')
    else:
        return HttpResponse('Activation link is invalid!')


# I want to restrict certain views so that only logged-in users can access them
class PrivatePageView(LoginRequiredMixin, TemplateView):
    template_name = 'private_page.html'


# Access Controls & Authentication
@login_required
def dashboard(request):
    # Show user’s private dashboard
    return render(request, 'accounts/dashboard.html')


# View for editing profile
@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})
