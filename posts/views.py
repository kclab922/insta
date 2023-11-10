from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    posts = Post.objects.all().order_by('-id')
    form = CommentForm()

    context = {
        'posts': posts,
        'form': form,
    }
    
    return render(request, 'index.html', context)


def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:index')
    else:
        form = PostForm()
    
    context = {
        'form': form,
    }

    return render(request, 'form.html', context)


@login_required
def delete(request, id):
    post = Post.objects.get(id=id)

    if request.user == post.user:
        post.delete()
    
    return redirect('posts:index')


@login_required
def update(request, id):
    post = Post.objects.get(id=id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
    }

    return render(request, 'form.html', context)


@login_required
def likes(request, id):
    # 현재 로그인한 사람의 정보 저장
    user = request.user
    post = Post.objects.get(id=id)

    # 이미 좋아요 버튼이 눌려있는 경우
    # if post in user.like_posts.all():
    if user in post.like_users.all():
        post.like_users.remove(user)
        
    # 좋아요 버튼을 아직 안 누른 경우
    else:
        # 게시물에.좋아요버튼누른사람 컬럼에 .현재 로그인한사람을 추가하는 과정
        # 둘중 하나만 추가해도 연동이 되어있으므로 ...  어쨌든 user 랑 post에 각각 할당되는 것
        # user.like_posts.add(post)
        post.like_users.add(user)
    
    return redirect('posts:index')


@login_required
def comment_create(request, post_id):
    form = CommentForm(request.POST)    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user_id = request.user.id
        comment.post_id = post_id
        comment.save()
        return redirect('posts:index')

@login_required
def comment_delete(request, post_id, id):
    comment = Comment.objects.get(id=id)

    if request.user == comment.user:
        comment.delete()
    
    return redirect('posts:index')