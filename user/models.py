from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
#摘要获取
from django.utils.html import strip_tags

class Category(models.Model):
    class Meta:
        db_table = 'category'
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    class Meta:
        db_table = 'tag'
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    class Meta:
        db_table = 'post'
        ordering = ['-created_time']
    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag,blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.title

# 从django.urls 中导入reverse函数,将pk传入url
    def get_absolute_url(self):
        return reverse('user:detail',kwargs={'pk':self.pk})
    # 新增views字段记录阅读量
    views = models.PositiveIntegerField(default=0)
    # 每调用一次views数值+1
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 自动提取文章前54个字符为摘要
    def save(self,*args,**kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54] + '......'

        super(Post,self).save(*args,**kwargs)
