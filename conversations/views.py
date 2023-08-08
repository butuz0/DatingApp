from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import Conversation
from .forms import CreateMessageForm


# Create your views here.
@login_required
def all_conversations(request):
    conversations = Conversation.objects.filter(users__in=[request.user.id])
    return render(request, 'conversation/all_conversations.html', context={'conversations': conversations})


@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation.objects
                                     .filter(users__in=[request.user.id])
                                     .get(id=conversation_id))

    if request_method == 'POST':
        message_form = CreateMessageForm(request.POST)
        message_form.conversation = conversation
        message_form.created_by = request.user
        return redirect('conversation:conversation_detail', id=conversation_id)

    return render(request, 'conversations/detail.html', {'conversation': conversation})
