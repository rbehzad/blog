from django.http.response import HttpResponse
from django.views.generic import ListView
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from post.models import Category, Post
from django.contrib.auth.decorators import login_required

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


# login
@login_required(login_url='login')
def dashboard(request):
    user = request.user
    return render(request, 'post/dashboard.html', {})

def logoutUser(request):
    logout(request)
    return redirect('login')

def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # if user authenticated below function return user object
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # this is gonna create that session and put into that coockies
            login(request, user)
            return redirect('dashboard')

    return render(request, 'post/login_register.html')
