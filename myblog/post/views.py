from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView

from post.models import Category, Post


class HomeListView(ListView):
    model = Post
    template_name = 'home.html'
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
    return render(request, 'post_detail.html', context)


def class_category(request, slug_text):
    cate = Category.objects.get(slug=slug_text)
    posts = Post.objects.filter(category=cate)
    categories = Category.objects.all()

    context = {
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'category.html', context)
