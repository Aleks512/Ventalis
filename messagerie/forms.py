from django import forms


class ThreadForm(forms.Form):
  username = forms.CharField(label='', max_length=100) #we need to input a username of the person we want to talk to
class MessageForm(forms.Form):
  message = forms.CharField(label='', max_length=1000) # a message thread that will have a text box for the message

class Register(forms.Form):
  user_name = forms.CharField(label="Your name", max_length=100)
  email = forms.EmailField()
  password = forms.CharField(widget = forms.PasswordInput())