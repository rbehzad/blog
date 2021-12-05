from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import ListView

from post.models import Category, Post, Tag

from .forms import AddPost, CustomUserCreationForm


class HomeListView(ListView):
    model = Post
    template_name = 'post/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-created_at')
        context['categories'] = Category.objects.all()
        return context

def post_detail(request, slug_text):
    post = Post.objects.filter(slug = slug_text)
    categories = Category.objects.all()
    if post.exists():
        post = post.first()
    else:
        return HttpResponse('<h1>Page Not Found</h1>')

    comments = post.comment_set.all()
    context = {
        'post': post,
        'comments': comments,
        'categories': categories,
    }

    return render(request, 'post/post_detail.html', context)

def class_category(request, slug_text):
    cate = Category.objects.get(slug=slug_text)
    posts = Post.objects.filter(category=cate)
    categories = Category.objects.all()

    context = {
        'posts': posts,
        'categories': categories,
    }

    return render(request, 'post/category.html', context)


# login + logout + register
@login_required(login_url='login')
def dashboard(request):
    user = request.user
    posts = Post.objects.filter(author=user)
    categories = Category.objects.all()
    context = {'posts': posts, 'categories': categories}
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
            return redirect('dashboard')

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
                return redirect('dashboard')
        
    context = {'form': form, 'page': page}
    return render(request, 'post/login_register.html', context)

@login_required(login_url='login')
def addPost(request):
    categories = Category.objects.all()
    form = AddPost()
    if request.method == 'POST':
        form = AddPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            post.save()
            return HttpResponseRedirect('dashboard')
    else:
        if 'submitted' in request.GET:
            submitted = True

    context = {'categories': categories, 'form': form}
    return render(request, 'post/add_post.html', context)




# @login_required(login_url='login')
# def addPost(request):
#     categories = Category.objects.all()
#     tags = Tag.objects.all()

#     if request.method == 'POST':
#         data = request.POST
#         images = request.FILES.getlist('images') # return a list
        
#         if data['category'] != 'none':
#             category = Category.objects.get(id=data['category'])
#         elif data['category_new'] != '':
#             category = Category.objects.get_or_create(
#                 name=data['category_new'])

#         post = Post.objects.create(
#             author=request.user,
#             content=data['content'],
#             category=category,
#             title=data['title'],
#             image=images[0],
#         )

#         return redirect('dashboard')

#     context = {'categories': categories, 'tags': tags}
#     return render(request, 'post/add_post.html', context)
