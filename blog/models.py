from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Tag(models.Model):
    """
    博文标签类
    """
    tag_name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 博主

    def __unicode__(self):
        return self.tag_name

    def __str__(self):
        return self.tag_name


class Category(models.Model):
    """
    博文分类
    """
    category_name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 博主

    def __unicode__(self):
        return self.category_name

    def __str__(self):
        return self.category_name


class Article(models.Model):
    """
    博文
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 博主
    title = models.CharField(max_length=100)  # 博客题目
    category = models.ForeignKey(Category, related_name="article")  # 博文分类
    tag = models.ManyToManyField(Tag, blank=True)  # 博客标签 可为空
    date_time = models.DateTimeField(auto_now_add=True)  # 博客日期
    content = models.TextField(blank=True, null=True)  # 博客文章正文

    def get_absolute_url(self):
        path = reverse('blog:detail', kwargs={'id': self.id})
        return "http://127.0.0.1:8000%s" % path

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_time']
