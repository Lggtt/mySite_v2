from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from my_messages.models import Message


#View to send a message
@login_required
def send_message(request, username):
    recipient = User.objects.get(username=username)
    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(sender=request.user, recipient=recipient, content=content)
        return redirect('my_messages:inbox')
    return render(request, 'messages/send.html', {'recipient': recipient})


#Inbox view
@login_required
def inbox(request):
    messages_received = request.user.received_messages.all().order_by('-timestamp')
    return render(request, 'messages/inbox.html', {'my_messages': messages_received})


def send_message_view(request):
    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        # TODO: Implement logic to create/save message model
        # e.g., Message.objects.create(sender=request.user, recipient=recipient, subject=subject, body=body)
        messages.success(request, 'Your message has been sent!')
        return redirect('inbox')  # or wherever you want to go next
    return render(request, 'messages/send.html')
