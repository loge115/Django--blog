from django.shortcuts import render,get_object_or_404

# Create your views here.
from django.http import HttpResponse
from comments.form import CommentForm
from .models import Post,Category,Tag
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView,DetailView

from django.db.models import Q
def search(request):
    # q与搜索网页中搜索框input的name属性的值一致
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = '请输入关键词'
        return render(request,'index.html',{'error_msg':error_msg})
    post_list = Post.objects.filter(Q(title__icontains=q)|Q(body__icontains=q))
    return render(request,'index.html',{'error_msg':error_msg,
                                        'post_list':post_list})

class IndexView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'post_list'
    # 分页设置
    paginate_by = 2
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator,page,is_paginated)

        context.update(pagination_data)
        return context
    def pagination_data(self,paginator,page,is_paginated):
        if not is_paginated:
            return {}
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range
        if page_number ==1:
            right = page_range[page_number:page_number+2]
            if right[-1]< total_pages -1:
                right_has_more = True
            if right[-1]<total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3)> 0 else 0:page_number - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] >1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3)> 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages -1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        data = {
            'left':left,
            'right':right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last,
        }
        return data
# def index(request):
#     post_list =Post.objects.all()
#     return render(request,'index.html',
#                   context={'title':'loge的博客主页',
#                            'welcome':'欢迎访问我的博客首页',
#                            'post_list':post_list})

#post内容视图
class PostDetailView(DetailView):
    model = Post
    template_name = 'single.html'
    context_object_name = 'post'
    def get(self,request,*args,**kwargs):
        response = super().get(request,*args,**kwargs)
        self.object.increase_views()
        return response
    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions = [
                                            'markdown.extensions.extra',
                                            #语法高亮拓展
                                            'markdown.extensions.codehilite',
                                            #自动生成目录
                                            TocExtension(slugify = slugify),
                                      ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({'form':form,
                        'comment_list':comment_list})
        return context
# def detail(request,pk):
#     post = get_object_or_404(Post,pk=pk)
#     post.increase_views()
#     post.body = markdown.markdown(post.body,
#                                   extensions = [
#                                       'markdown.extensions.extra',
#                                       #语法高亮拓展
#                                       'markdown.extensions.codehilite',
#                                       'markdown.extensions.toc',
#                                   ])
#     form = CommentForm()
#     comment_list = post.comment_set.all()
#     context = {'post': post,
#                'form': form,
#                'comment_list': comment_list
#                }
#     return render(request, 'single.html', context=context)
#     # return render(request,'single.html',context={'post':post})

# 归档视图
class ArchivesView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super().get_queryset().filter(created_time__year = year,
                                                created_time__month = month)

# def archives(request,year,month):
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month)
#     return render(request,'index.html',context={'post_list':post_list})

# 分类视图
class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category,pk = self.kwargs.get('pk'))
        return super().get_queryset().filter(category = cate)
# def category(request,pk):
#     cate = get_object_or_404(Category,pk=pk)
#     post_list = Post.objects.filter(category=cate)
#     return render(request,'index.html',context={'post_list':post_list})

class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag,pk = self.kwargs.get('pk'))
        return super().get_queryset().filter(tag = tag)