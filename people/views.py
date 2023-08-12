from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages


# Create your views here.
@login_required
def list_people(request):
    current_user = request.user.user_info
    people = UserInfo.objects.filter(preferences__in=['BOTH', current_user.gender])
    if current_user.preferences != 'BOTH':
        people = people.exclude(gender=current_user.gender)
    return render(request, 'people/list.html', {'current_user': current_user,
                                                'people': people})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'people/detail.html', {'user': user})


@login_required
@require_POST
def like_user(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'like':
                like = Like.objects.get_or_create(user_from=request.user, user_to=user)[0]
                print(like)
                if like.match():
                    messages.success(request, 'Its a match!')

            else:
                Like.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})

        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'error'})


@login_required
def user_activity(request):
    likes_list = Like.objects.filter(Q(user_from=request.user) | Q(user_to=request.user))
    return render(request, 'people/user_activity.html', {'likes_list': likes_list})
