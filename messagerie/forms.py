from django import forms


class ThreadForm(forms.Form):
  email = forms.CharField(label='', max_length=100) #we need to input a username of the person we want to talk to
class MessageForm(forms.Form):
  message = forms.CharField(label='', max_length=1000) # a message thread that will have a text box for the message

