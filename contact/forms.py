from django import forms
from django.conf import settings
from django.core.mail import send_mail

class ContactForm(forms.Form):

    nom = forms.CharField(max_length=120)
    email = forms.EmailField() #the email of the person who’s trying to contact me
    sujet = forms.CharField(max_length=70) #subject
    message = forms.CharField(widget=forms.Textarea)

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()

        nom = cl_data.get('nom').strip()
        from_email = cl_data.get('email')
        sujet = cl_data.get('sujet')

        msg = f'{nom} son email {from_email} nous dit:'
        msg += f'\n"{sujet}"\n\n'
        msg += cl_data.get('message')

        return sujet, msg

    def send(self):

        sujet, msg = self.get_info()

        send_mail(
            subject=sujet,
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.RECIPIENT_ADDRESS]
        )