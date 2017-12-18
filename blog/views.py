
from .models import Blog,Category
from django.shortcuts import render, get_object_or_404
import markdown
from comments.forms import CommentForm
# Create your views here.
def index(request):
    blog_list = Blog.objects.all().order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list': blog_list})

def detail(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {
                'post':post,
                'form':form,
                'comment_list':comment_list
            }
    return render(request, 'blog/detail.html', context=context)
def archives(request, year, month):
    post_list = Blog.objects.filter(created_time__year=year,
                                    created_time__month=month,
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Blog.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})