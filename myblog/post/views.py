from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import ListView

from post.models import Category, Post, Tag

from .forms import AddCategory, AddPost, AddTag, CustomUserCreationForm


class HomeListView(ListView):
    model = Post
    template_name = 'post/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-created_at')
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

def post_detail(request, slug_text):
    post = Post.objects.filter(slug = slug_text)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    if post.exists():
        post = post.first()
    else:
        return HttpResponse('<h1>Page Not Found</h1>')

    comments = post.comment_set.all()
    context = {
        'post': post,
        'comments': comments,
        'categories': categories,
        'tags': tags,
    }

    return render(request, 'post/post_detail.html', context)

def class_category(request, slug_text):
    category = Category.objects.get(slug=slug_text)
    posts = Post.objects.filter(category=category).order_by('-created_at')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        'posts': posts,
        'categories': categories,
        'tags': tags,
    }

    return render(request, 'post/category.html', context)


# login + logout + register
@login_required(login_url='login')
def dashboard(request):
    user = request.user
    posts = Post.objects.filter(author=user).order_by('-created_at')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        'posts': posts,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'post/dashboard.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

def loginUser(request):
    page = 'login'
    context = {'page': page}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # if user authenticated below function return user object
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # this is gonna create that session and put into that coockies
            login(request, user)
            return redirect(dashboard)

    return render(request, 'post/login_register.html', context)

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect(dashboard)
        
    context = {'form': form, 'page': page}
    return render(request, 'post/login_register.html', context)

@login_required(login_url='login')
def addPost(request):
    page = 'add_post'
    categories = Category.objects.all()
    tags = Tag.objects.all()
    form = AddPost()
    if request.method == 'POST':
        form = AddPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect(dashboard)
    else:
        if 'submitted' in request.GET:
            submitted = True

    context = {'categories': categories, 'form': form, 'page': page, 'tags': tags}
    return render(request, 'post/add_update.html', context)


@login_required(login_url='login')
def addCategory(request):
    page = 'add_category'
    categories = Category.objects.all()
    tags = Tag.objects.all()
    form = AddCategory()
    if request.method == 'POST':
        form = AddCategory(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('categories')
    else:
        if 'submitted' in request.GET:
            submitted = True

    context = {'categories': categories, 'form': form, 'page': page, 'tags': tags}
    return render(request, 'post/add_update.html', context)


@login_required(login_url='login')
def addTag(request):
    page = 'add_tag'
    categories = Category.objects.all()
    tags = Tag.objects.all()
    form = AddTag()
    if request.method == 'POST':
        form = AddTag(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.save()
            return redirect('tags')
    else:
        if 'submitted' in request.GET:
            submitted = True

    context = {'form': form, 'page': page, 'categories': categories, 'tags': tags}
    return render(request, 'post/add_update.html', context)


@login_required(login_url='login')
def categoryList(request):
    page = 'categories'
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        'categories': categories,
        'tags': tags,
        'page': page,
    }
    return render(request, 'post/delete_updateButton.html', context)


@login_required(login_url='login')
def deleteCategory(requset, slug):
    category = Category.objects.get(slug=slug)
    category.delete()
    return redirect('categories')


@login_required(login_url='login')
def updateCategory(request, slug):
    page = 'update_category'
    categories = Category.objects.all()
    tags = Tag.objects.all()
    category = Category.objects.get(slug=slug)
    form = AddCategory()
    if request.method == 'POST':
        form = AddCategory(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')

    context = {'form': form, 'page': page, 'categories': categories, 'tags': tags}
    return render(request, 'post/add_update.html', context)


@login_required(login_url='login')
def tagList(request):
    page = 'tags'
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        'categories': categories,
        'tags': tags,
        'page': page,
    }
    return render(request, 'post/delete_updateButton.html', context)


@login_required(login_url='login')
def deleteTag(request, slug):
    tag = Tag.objects.get(slug=slug)
    tag.delete()
    return redirect('tags')


@login_required(login_url='login')
def updateTag(request, slug):
    page = 'update_tag'
    categories = Category.objects.all()
    tags = Tag.objects.all()
    tag = Tag.objects.get(slug=slug)
    form = AddTag()
    if request.method == 'POST':
        form = AddTag(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('tags')

    context = {'form': form, 'page': page, 'categories': categories, 'tags': tags}
    return render(request, 'post/add_update.html', context)