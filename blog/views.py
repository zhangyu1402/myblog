
from .models import Blog,Category
from django.shortcuts import render, get_object_or_404
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView,DetailView

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
    post.increase_views()
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
                                    
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Blog.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

class IndexView(ListView):
    model = Blog
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 1

class CategoryView(ListView):
    model = Blog
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        cate = get_object_or_404(Category,pk = self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(category = cate)

class ArchivesView(IndexView):

    def get_queryset(self):
        return super().get_queryset().filter(created_time__year=self.kwargs.get('year'),
                                    ).order_by('-created_time')


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self,request,*args,**kwargs):
        response = super().get(request,*args,**kwargs)
        self.object.increase_views()
        return response

    def get_object(self,queryset = None):
        post = super().get_object(queryset = None)
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context

class TagView(ListView):
    model = Blog
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)