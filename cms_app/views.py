from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category, Comment, Reply
from .forms import CreatePostForm, UpdatePostForm, CommentForm, ReplyForm
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Count



# Create your views here.
def index(request):
    categories = Category.objects.all()
    search_querry = ''
    if request.GET.get('search'):
        search_querry = request.GET.get('search')
        category = Category.objects.filter(title__icontains = search_querry)
        posts = Post.objects.distinct().filter(Q(title__icontains = search_querry) | Q(body__icontains = search_querry) |Q(category__in = category)).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')

    
    page = request.GET.get('page', 1)
    
    paginator = Paginator(posts, 6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts':posts,
        'categories':categories,
        'search_querry':search_querry
    }
    return render(request, 'index.html', context)





def detail_post(request, slug):
    categories = Category.objects.all()
    post = get_object_or_404(Post, slug=slug)
    posts = Post.objects.exclude(sno__exact=post.sno).order_by('-created_at')[:5]
    comment_form = CommentForm()
    reply_form = ReplyForm()
    approved_comments_count = post.comments.filter(status=True).count()
    approved_replies_count = post.comments.filter(replies__status=True).aggregate(reply_count=Count('replies'))['reply_count']

    if request.method == 'POST':
        if 'comment_form' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.status = False  # Set status to False
                comment.save()
                messages.success(request, 'Comment posted. It will be visible after admin approval.')
                return redirect('detail-post', slug=post.slug)

        elif 'reply_form' in request.POST:
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.author = request.user
                reply.comment = get_object_or_404(Comment, pk=request.POST['parent_id'])
                reply.status = False  # Set status to False
                reply.save()
                messages.success(request, 'Reply posted. It will be visible after admin approval.')
                return redirect('detail-post', slug=post.slug)

    return render(request, 'detail_post.html', {'post': post, 'posts': posts, 'categories':categories, 'comment_form': comment_form, 'reply_form': reply_form, 'approved_comments_count': approved_comments_count, 'approved_replies_count': approved_replies_count})

@login_required(login_url='login')
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.status = False  
            comment.save()
            messages.success(request, 'Comment posted. It will be visible after admin approval.')
    return redirect('detail-post', slug=post.slug)

@login_required(login_url='login')
def add_reply(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.comment = comment
            reply.status = False  
            reply.save()
            messages.success(request, 'Reply posted. It will be visible after admin approval.')
    return redirect('detail-post', slug=comment.post.slug)


def like_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.likes.add(request.user)
    comment.dislikes.remove(request.user)
    total_likes = comment.likes.count()
    total_dislikes = comment.dislikes.count()
    return JsonResponse({'total_likes': total_likes, 'total_dislikes': total_dislikes})

def dislike_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.likes.remove(request.user)
    comment.dislikes.add(request.user)
    total_likes = comment.likes.count()
    total_dislikes = comment.dislikes.count()
    return JsonResponse({'total_likes': total_likes, 'total_dislikes': total_dislikes})


def like_reply(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)

    if request.user in reply.dislikes.all():
        reply.dislikes.remove(request.user)

    reply.likes.add(request.user)
    
    total_likes = reply.likes.count()
    total_dislikes = reply.dislikes.count()

    return JsonResponse({'total_likes': total_likes, 'total_dislikes': total_dislikes})


def dislike_reply(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)

    if request.user in reply.likes.all():
        reply.likes.remove(request.user)

    reply.dislikes.add(request.user)
    
    total_likes = reply.likes.count()
    total_dislikes = reply.dislikes.count()

    return JsonResponse({'total_likes': total_likes, 'total_dislikes': total_dislikes})

def category_post(request, slug):
    category = get_object_or_404(Category, slug=slug)
    categories = Category.objects.all()
    posts = Post.objects.filter(category=category).order_by('-created_at')
    context = {
        'categories':categories,
        'category': category,
        'posts': posts
    }
    return render(request, 'category_post.html', context)



@login_required(login_url='login')
def create_post(request):
    profile = request.user.userprofile
    form = CreatePostForm()
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid:
            var = form.save(commit=False)
            var.slug = slugify(var.title)
            var.author = profile
            var.save()
            messages.success(request, 'post created succefully')
            return redirect('index')
        else:
            messages.warning(request, 'Something went wrong!')
            return redirect('create-post')
    else:
        form = CreatePostForm()
    context = {
        'form':form,
    }
    return render(request, 'create_post.html', context)

@login_required(login_url='login')
def update_post(request, slug):
    post = Post.objects.get(slug=slug)
    if request.user == post.author.user:
        if request.method == 'POST':
            form = UpdatePostForm(request.POST, request.FILES, instance=post) 
            if form.is_valid():
                form.save()
                messages.success(request, 'post updated succefully')
                return redirect('detail-post', slug=post.slug)
            else:
                messages.warning(request, 'Something went wrong!')
                return redirect('update-post')
            
        else:
            form = UpdatePostForm(instance=post)
        context = {
            'form':form,
            'post':post,
        }
        return render(request, 'update_post.html', context)
    else:
        messages.warning(request, "Sorry you do not have permission to update a post you didn't create")
        return redirect('index')

@login_required(login_url='login')
def delete_post(request, slug):
    post = Post.objects.get(slug=slug)
    if request.user == post.author.user:
        form = UpdatePostForm(instance=post)
        if request.method == 'POST':
            post.delete()
            messages.success(request, 'post deleted succefully')
            return redirect('index')
        context = {
            'form':form,
            'post':post,
        }
        return render(request, 'delete_post.html', context)
    else:
        messages.warning(request, "Sorry you do not have permission to delete a post you didn't create")
        return redirect('index')

    
    


