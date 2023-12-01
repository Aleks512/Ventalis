from django.shortcuts import render
from django.contrib import messages
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send the email
            try:
                form.send()  # Form method to send email
                messages.success(request, 'Merci pour votre message ! Nous vous répondrons sous peu.')
                # Clear the form after successful submission.
                form = ContactForm()
            except Exception as e:
                # Log the error, or use a messaging system to inform the user/email wasn't sent
                messages.error(request, 'Désolé, une erreur s\'est produite lors de l\'envoi de votre message. Veuillez réessayer plus tard..')
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})