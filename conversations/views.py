from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Conversation, Message
from account.models import Like
from .forms import CreateMessageForm


# Create your views here.
@login_required
def all_conversations(request):
    conversations = Conversation.objects.filter(users__in=[request.user.id])
    return render(request, 'conversations/all_conversations.html',
                  context={'conversations': conversations})


@login_required
def conversation_detail(request, user_id):
    person = User.objects.get(id=user_id)
    allow_conversation = True

    try:
        like = Like.objects.get(user_from=request.user, user_to=person)
    except Like.DoesNotExist:
        allow_conversation = False
    else:
        if not like.match():
            allow_conversation = False

    if not allow_conversation:
        return render(request, 'conversations/conversation_details.html', {'person': person,
                                                                           'allow_conversation': allow_conversation})

    try:
        conversation = Conversation.objects.filter(users__in=[str(request.user.id)]).filter(users__in=[user_id]).get()
    except Conversation.DoesNotExist:
        conversation = Conversation.objects.create()
        conversation.users.add(str(request.user.id))
        conversation.users.add(user_id)
        conversation.save()

    if request.method == 'POST':
        message_form = CreateMessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.conversation = conversation
            conversation.update()
            message.created_by = request.user
            message.save()
        return redirect('conversations:conversation_detail', user_id=user_id)

    else:
        message_form = CreateMessageForm()
        # set all unread messages sent by other user as read
        Message.objects.filter(conversation=conversation, created_by=user_id,
                               message_read=False).update(message_read=True)

    return render(request, 'conversations/conversation_details.html', {'conversation': conversation,
                                                                       'message_form': message_form,
                                                                       'person': person,
                                                                       'allow_conversation': allow_conversation})
