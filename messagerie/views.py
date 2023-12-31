from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from messagerie.forms import ThreadForm, MessageForm
from messagerie.models import ThreadModel, MessageModel
from users.models import NewUser
from django.contrib import messages



@method_decorator(login_required, name='dispatch')
class CreateThread(View):
    # display the form to enter a user name
    def get(self, request, *args, **kwargs):
        form = ThreadForm()
        context = {
            'form': form
        }
        return render(request, 'messagerie/create_thread.html', context)
    # handle creating the thread
    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        email = request.POST.get('email')
        try:
            receiver = NewUser.objects.get(email=email)
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
            messages.error(request, "Cet utilisateur n'existe pas")
            return redirect('create-thread')

@method_decorator(login_required, name='dispatch')
class ListThreads(View):
  def get(self, request, *args, **kwargs):
    threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))
    messages = []

    for thread in threads:
        message = MessageModel.objects.filter(thread=thread).last()
        messages.append(message)

    context = {
        'threads': threads,
        'messages': messages,
    }
    return render(request, 'messagerie/inbox.html', context)
@method_decorator(login_required, name='dispatch')
class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = get_object_or_404(ThreadModel, pk=pk)
        # Vérifier si l'utilisateur fait partie du thread
        if request.user == thread.user or request.user == thread.receiver:
            message_list = MessageModel.objects.filter(thread__pk__contains=pk)
            context = {
                'thread': thread,
                'form': form,
                'message_list': message_list
            }
            return render(request, 'messagerie/thread.html', context)
        else:
            return HttpResponseForbidden('Unauthorized', status=401)

@method_decorator(login_required, name='dispatch')
class CreateMessage(View):
  def post(self, request, pk, *args, **kwargs):
    thread = ThreadModel.objects.get(pk=pk)

    if thread.receiver == request.user: #qui est athentifié et recois le maessage
      receiver = thread.receiver #qui est athentifié et recois le maessage
      message = MessageModel(
        thread=thread,
        sender_user=request.user,
        receiver_user=receiver,
        body=request.POST.get('message'),
      )
      message.save()
      return redirect('thread', pk=pk)
    if thread.user == request.user:
      receiver = thread.user
      message = MessageModel(
        thread=thread,
        sender_user=request.user,
        receiver_user=receiver,
        body=request.POST.get('message'),
      )
      message.save()
      return redirect('thread', pk=pk)

