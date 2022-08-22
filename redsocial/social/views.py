from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Relationship
from .forms import PostForm, UserRegisterForm
from django.contrib.auth.models import User

def feed(request):
    posts=Post.objects.all()
    return render(request,'social/feed.html', {"posts":posts})

def profile(request):
    return render(request, 'social/profile.html' )

def register(request):
    if request.method=="POST":
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            messages.success(request, "Usuario creado correctamente")
            return redirect('feed')
    else:
        form=UserRegisterForm()
    return render(request, 'social/register.html',{"form":form,})

def post(request):
    current_user = get_object_or_404(User, pk=request.user.pk)
    if request.method=="POST":
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=current_user
            post.save()
            messages.success(request, "Su post se envió correctamente")
            return redirect('feed')
    else:
        form=PostForm()
        return render(request, 'social/post.html',{"form":form})

def profile(request, username=None): #le paso de parametro username para modificar la URL
    current_user=request.user #el usuario que pidio la petición
    if username and username != current_user.username:
        user=User.objects.get(username=username)#le digo que busque en la base de datos el username del parametro
        posts=user.posts.all() #traigo todos los posts del user
    else:
        posts=current_user.posts.all()
        user=current_user

    return render(request, 'social/profile.html',{'user':user, 'posts':posts})

def follow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user
	rel = Relationship(from_user=current_user, to_user=to_user_id)
	rel.save()
	messages.success(request, f'sigues a {username}')
	return redirect('feed')

def unfollow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user.id
	rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id).get()
	rel.delete()
	messages.success(request, f'Ya no sigues a {username}')
	return redirect('feed')


