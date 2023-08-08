from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Conversation, Message
from .forms import CreateMessageForm


# Create your views here.
@login_required
def all_conversations(request):
    conversations = Conversation.objects.filter(users__in=[request.user.id])
    return render(request, 'conversations/all_conversations.html', context={'conversations': conversations})


@login_required
def conversation_detail(request, user_id):
    try:
        conversation = Conversation.objects.filter(users__in=str(request.user.id)).filter(users__in=user_id).get()
        print(conversation)
    except Conversation.DoesNotExist:
        print('conversation does not exist')
        conversation = Conversation.objects.create()
        conversation.users.add(str(request.user.id), user_id)

    if request.method == 'POST':
        message_form = CreateMessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.conversation = conversation
            message.created_by = request.user
            message.save()
        return redirect('conversations:conversation_detail', user_id=user_id)

    else:
        message_form = CreateMessageForm()

    return render(request, 'conversations/detail.html', {'conversation': conversation,
                                                         'message_form': message_form})
