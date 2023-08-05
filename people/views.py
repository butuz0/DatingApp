from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.models import Profile


# Create your views here.
@login_required
def list_people(request):
    current_user = request.user.profile
    people = Profile.objects.filter(preferences__in=['BOTH', current_user.gender])
    if current_user.preferences != 'BOTH':
        people = people.exclude(gender=current_user.gender)
    return render(request, 'people/list.html', {'current_user': current_user,
                                                'people': people})
