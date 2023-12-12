from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def home_page(request):
    return redirect('people:list_people')
