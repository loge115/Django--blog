from django.contrib.syndication.views import Feed
from .models import Post

class ALLPostsRssFeed(Feed):
    # 显示聚合器上阅读的标题
    title = 'Log\'s island'

    # 通过聚合阅读器跳转到网站的地址
    link = '/'

    # 显示聚合器上的描述信息
    description = 'loge博客内容测试文章'

    #需要显示的内容条目
    def items(self):
        return Post.objects.all()

    #聚合器中显示的内容条目的标题
    def item_title(self, item):
        return '[%s]%s' % (item.category,item.title)

    #聚合器中显示的内容条目的描述
    def item_description(self, item):
        return item.body