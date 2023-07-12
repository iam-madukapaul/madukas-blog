from django.shortcuts import render, redirect
from django.contrib import messages
from . forms import ContactForm
from cms_app.models import Category

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# Create your views here.
def contact(request):
    categories = Category.objects.all()
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            message = form.cleaned_data.get('message')
            html = render_to_string('contact/contactmessage.html', {
                'name': name,
                'email': email,
                'phone': phone,
                'message': message,
            })
            send_mail('Contact Us', html, settings.DEFAULT_FROM_EMAIL, ['madukasblog@gmail.com'], fail_silently=False, html_message=html)
            messages.success(request, "Thank you for reaching us, we'll get back to you shortly.")
            return redirect('contact')
        else:
            messages.info(request, "Something went wrong, please try again.")

    else:
        form = ContactForm()
    context = {
        'categories':categories,
        'form': form,
    }
    return render(request, 'contact.html', context)

