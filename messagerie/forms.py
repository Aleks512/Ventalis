from django import forms



class ThreadForm(forms.Form):
    email = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

class MessageForm(forms.Form):
    message = forms.CharField(label='', max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
