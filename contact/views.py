from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactForm


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email code goes here
            send_mail(
                'Contact Form',
                message,
                email,
                ['admin@example.com'],  # Replace with your email
                fail_silently=False,
            )

            return render(request, 'contact_thanks.html')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

