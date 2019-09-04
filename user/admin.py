from django.contrib import admin

# Register your models here.
from user.models import Category,Post,Tag
# 设定选定post界面窗口
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','created_time','modified_time','category','author']
    ordering = ['modified_time']

#新增注册内容

admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)