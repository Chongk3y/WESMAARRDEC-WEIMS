from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from .forms import CommentForm, CategoryForm, FactForm
from .models import Post, Category, Fact, PostImages, Comment
from cmscore.models import Album, AlbumPhoto
from program.models import Program
from django.utils.text import slugify
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import connection
from django.core.paginator import Paginator
from .forms import FactForm, CategoryForm, PostForm
from cmscore.forms import SearchForm
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Post
from cmscore.decorators import secretariat_required

def posts(request, cat):
    # Get the category using the slug
    category = get_object_or_404(Category, slug=cat)

    # Filter posts by the category and status
    posts = Post.objects.filter(category=category, status=Post.ACTIVE)

    # Set up pagination
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Create the context
    context = {
        'title': 'Posts',
        'posts': posts,
        'page_obj': page_obj,
        'category': category  # Pass the category for additional context
    }

    return render(request, "posts.html", context)


def AllPosts(request):
    program = Program.objects.all()
    events = Post.objects.all()  # Filter posts by category and status
    paginator = Paginator(events, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'All Posts',
        'programs' : program,
        'events': events,
        'page_obj': page_obj
    }
    return render(request, "allposts.html", context)

@login_required
def MyPosts(request):
    program = Program.objects.all()
    events = Post.objects.filter(author=request.user)  # Filter posts by author
    paginator = Paginator(events, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'My Posts',
        'programs' : program,
        'events': events,
        'page_obj': page_obj
    }
    return render(request, "myposts.html", context)

def detail(request, category_slug, slug):
    category = get_object_or_404(Category, slug=category_slug)
    post = get_object_or_404(Post, slug=slug, category=category)
    latest_posts = Post.objects.all().order_by('-created_at')[:5]
    comments = post.comments.all()
    title = post.title
    paginator = Paginator(comments, 5)  # Show 5 comments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.name = request.user
            new_comment.save()
            form = CommentForm()  # Clear the form
    else:
        form = CommentForm()

    search_form = SearchForm(request.GET or None)
    context = {
        'title' : title,
        'latest_posts': latest_posts,
        'comments': page_obj,
        'category': category,
        'comment_count': comments.count(),
        'post': post,
        'form': form,
        'is_paginated': page_obj.has_other_pages()
    }
    return render(request, "detail.html", context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('myposts')
    else:
        form = PostForm()
    return render(request, 'createposts.html', {'form': form})

@login_required
def delete_postcms(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('myposts')  # Redirect to post list after deletion
    return render(request, 'delete_post.html', {'post': post})


def view_posts(request):
    categories = Category.objects.annotate(post_count=Count('posts')).all()
    posts = Post.objects.all()
    facts = Fact.objects.all()
    category_filter = request.GET.get('category')
    query = request.GET.get('q')

    if category_filter:
       posts = posts.filter(category__title=category_filter)
    if query:
        posts = posts.filter
        (
            Q(title__icontains=query) |
            Q(author__icontains=query)
            )

    paginator = Paginator(posts, 10)  # Show 10 sites per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title' : "Manage Posts",
        'page_obj': page_obj,
        'categories': categories,
        'facts' : facts
    }
    return render(request, 'view_posts.html', context)

@secretariat_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('view_posts')
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})

@secretariat_required
def add_fact(request):
    if request.method == 'POST':
        form = FactForm(request.POST, request.FILES)
        if form.is_valid():
            fact = form.save(commit=False)
            fact.created_by = request.user.username
            fact.save()
            return redirect('view_posts')
    else:
        form = FactForm()
    return render(request, 'add_fact.html', {'form': form})

@secretariat_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user.username
            category.save()
            return redirect('view_posts')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

@secretariat_required
@login_required
def edit_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('view_posts')  # redirect to post list view
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form, 'post': post})

@secretariat_required
@login_required
def edit_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('view_posts')  # redirect to category list view
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form, 'category': category})

@secretariat_required
@login_required
def edit_fact(request, fact_id):
    fact = Fact.objects.get(pk=fact_id)
    if request.method == 'POST':
        form = FactForm(request.POST, request.FILES, instance=fact)
        if form.is_valid():
            form.save()
            return redirect('view_posts')  # redirect to fact list view
    else:
        form = FactForm(instance=fact)
    return render(request, 'edit_fact.html', {'form': form, 'fact': fact})

@secretariat_required
def delete_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('view_posts')  # Redirect to category list after deletion
    return render(request, 'delete_category.html', {'category': category})

@secretariat_required
def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('View_posts')  # Redirect to post list after deletion
    return render(request, 'delete_post.html', {'post': post})

@secretariat_required
def delete_fact(request, fact_id):
    fact = Fact.objects.get(pk=fact_id)
    if request.method == 'POST':
        fact.delete()
        return redirect('View_posts')  # Redirect to fact list after deletion
    return render(request, 'delete_fact.html', {'fact': fact})

def delete_comment(request, comment_id):
    title = "delete comments"
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.name and request.user != post.author:
        return HttpResponseForbidden("You do not have permission to delete this comment.")
    if request.method == 'POST':
        comment.delete()
        return redirect('detail', category_slug=comment.post.category.slug, slug=comment.post.slug) # Redirect to the post detail view after deletion
    context = {
        'comment': comment,
        'title': title,
    }
    return render(request, 'delete_comment.html', context)

def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    # Check if the logged-in user is the author of the comment
    if request.user != comment.name:
        return redirect('detail', category_slug=comment.post.category.slug, post_slug=comment.post.slug)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('detail', category_slug=comment.post.category.slug, slug=comment.post.slug)
    else:
        form = CommentForm(instance=comment)

    context = {
        'form': form,
        'comment': comment
    }
    return render(request, 'edit_comment.html', context)
