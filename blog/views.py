# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .forms import PostForm

from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
def post_list(request):
    context = {}
    context['home_active'] = True
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = reversed(posts)
    context['posts'] = posts
    return render(request, 'blog/post_list.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {'post': post}
    context['post_detail_active]'] = True
    return render(request, 'blog/post_detail.html', context)

def post_new(request):
    context = {}
    context['new_post_active'] = True
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    context['form'] = form
    return render(request, 'blog/post_edit.html', context)

def post_edit(request, pk):
    context = {}
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        context['edit_post'] = "Edit post for "+ post.title
        form = PostForm(instance=post)
    context['form'] = form
    context['active_tab'] = True
    return render(request, 'blog/post_edit.html', context)