from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from messages.forms import ThreadForm
from django.contrib.auth import get_user_model
from messages.models import ThreadModel

User = get_user_model()
class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()
        context = {
            'form': form
        }
        return render(request, 'messages/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        email = request.POST.get('email')
        try:
            receiver = User.objects.get(email=email)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                sender_thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                sender_thread.save()
                thread_pk = sender_thread.pk
                return redirect('thread', pk=thread_pk)
        except:
            return redirect('create-thread')

class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))
        context = {'threads': threads}
        return render(request, 'social/inbox.html', context)
