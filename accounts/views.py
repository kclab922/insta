from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form': form
    }
    
    return render(request, 'accounts_form.html', context)


def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('posts:index')

    else:
        form = CustomAuthenticationForm()
    
    context = {
        'form': form
    }

    return render(request, 'accounts_form.html', context)


def logout(request):
    auth_logout(request)
    return redirect('accounts:login')


def profile(request, username):
    user_info = User.objects.get(username=username)

    context = {
        'user_info': user_info,
    }

    return render(request, 'profile.html', context)


@login_required
def follows(request, username):
    me = request.user
    you = User.objects.get(username=username)

    # 이미 팔로우중인 경우
    # if me in you.followers.all():
    if you in me.followings.all():
        me.followings.remove(you)

    # 아직 팔로우를 안 하고 있던 경우
    else:
        me.followings.add(you)

    return redirect('accounts:profile', username=username)


