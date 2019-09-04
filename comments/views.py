from django.shortcuts import render,get_object_or_404,redirect

# Create your views here.
from user.models import Post
from .models import Comment
from .form import CommentForm

def post_comment(request,pk):
    # 获取被评论文章
    post = get_object_or_404(Post,pk=pk)

    if request.method == 'POST':
        # 用户提交的数据存在request.POST中，是一个类字典对象
        form = CommentForm(request.POST)

        if form.is_valid():
            # commit=False表示利用表单数据生成Comment模型类的实例，不保存到数据库
            comment = form.save(commit=False)
            # 将评论和被评论文章关联起来
            comment.post = post

            comment.save()
            # 重新定向到post的页面，redirect接收一个模型实例，会调用实例get_absoulte_url方法
            # 重新定向到方法返回的url
            return redirect(post)
        else:
            # post.comment_set.all()等价于Comment.objects,filter(post=post)
            # post已有模型实例，故不使用后者
            comment_list = post.comment_set.all()
            context = {'post':post,
                       'form':form,
                       'comment_list':comment_list
                       }
        return render(request,'single.html',context=context)
    return redirect(post)