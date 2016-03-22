from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from .models import Article
from .models import Category
from .models import Tag
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse

def get_category_counter(user):
    """
    获得某用户博文目录及其该目录下文章个数
    """
    categories = Category.objects.filter(user=user)
    category_counter = dict()
    for category in categories:
        category_counter[category] = Article.objects.filter(user=user,
                                                            category_id=category.id).count()
    return category_counter


def get_tag_counter(user):
    """
    获得某用户博文标签及其该标签下文章个数
    """
    articles = Article.objects.filter(user=user).order_by('date_time')
    tag_counter = dict()
    for article in articles:
        for tag in article.tag.all():
            if tag not in tag_counter:
                tag_counter[tag] = 1
            else:
                tag_counter[tag] += 1
    return tag_counter

@login_required(login_url='/login')
def index_view(request):
    """
    博客主页
    """
    user = request.user
    articles = Article.objects.filter(user=user).order_by('date_time')
    paginator = Paginator(articles, 10)  # 每页显示个数
    
    # 统计分类中文章的个数
    category_counter = get_category_counter(user)
    
    # 获得使用到的标签
    tag_counter = get_tag_counter(user)
    
    page = request.GET.get('page')
    
    try:
        article_list = paginator.page(page)
    except PageNotAnInteger:
        article_list = paginator.page(1)
    except EmptyPage:
        article_list = paginator.paginator(paginator.num_pages)
    return render(request, 'blog/index.html', {'articles': articles,
                                               'category_counter': category_counter,
                                               'tag_counter': tag_counter})
    

@login_required(login_url='/login')
def detail_view(request, article_id):
    """
    博文页面
    """
    user = request.user
    article = get_object_or_404(Article, pk=article_id, user=user)
    
    # 统计分类中文章的个数
    category_counter = get_category_counter(user)
    
    # 获得使用到的标签
    tag_counter = get_tag_counter(user)
    
    return render(request, 'blog/article_detail.html', {'article': article,
                                                        'category_counter': category_counter,
                                                        'tag_counter': tag_counter})

@login_required(login_url='/login')
def new_article_view(request):
    """
    新建博文页面
    """
    user = request.user
    # 统计分类中文章的个数
    category_counter = get_category_counter(user)
    
    # 获得使用到的标签
    tag_counter = get_tag_counter(user)
    return render(request, 'blog/new_article.html', {'category_counter': category_counter,
                                                     'tag_counter': tag_counter})

@csrf_protect 
@login_required(login_url='/login')
def do_new_category(request):
    """
    新建分类
    """
    user = request.user
    try:
        category_name = request.POST['category_name']
        
        try:
            Category.objects.get(category_name=category_name)
            return HttpResponse('exist')
        except ObjectDoesNotExist as e:
            category = Category(user=user,
                                category_name=category_name)
            category.save()
            return HttpResponse(category.id)
    except KeyError as e:
        print(e)
        return HttpResponse('fail')

@csrf_protect 
@login_required(login_url='/login')    
def do_create_article(request):
    """
    新建文章
    """
    user = request.user
    try:
        title = request.POST['title']
        category_name = request.POST['category']
        tag_str = request.POST['tag']
        content = request.POST['content']
        
        category = Category.objects.get(user=user,
                                        category_name=category_name)
        
        article = Article(user=user,
                          title=title,
                          category=category,
                          content=content)
        
        if tag_str != '':
            tag_names = tag_str.strip().split(';')
            for tag_name in tag_names:
                tag = Tag.objects.get(user=user,
                                      tag_name=tag_name)
                article.tag.add(tag)
        
        article.save()
        
        # 统计分类中文章的个数
        category_counter = get_category_counter(user)
        
        # 获得使用到的标签
        tag_counter = get_tag_counter(user)
        
        return render(request, 'blog/article_detail.html', {'article': article,
                                                            'category_counter': category_counter,
                                                            'tag_counter': tag_counter,
                                                            'message': '新建文章成功'})
    except Exception as e:
        print(e)
        

@login_required(login_url='/login')
def do_show_articles_by_category(request, category_id):
    user = request.user
    articles = Article.objects.filter(user=user,
                                      category__id=category_id).order_by('date_time')
    paginator = Paginator(articles, 10)  # 每页显示个数
    
    # 统计分类中文章的个数
    category_counter = get_category_counter(user)
    
    # 获得使用到的标签
    tag_counter = get_tag_counter(user)
    
    page = request.GET.get('page')
    
    try:
        article_list = paginator.page(page)
    except PageNotAnInteger:
        article_list = paginator.page(1)
    except EmptyPage:
        article_list = paginator.paginator(paginator.num_pages)
    return render(request, 'blog/index.html', {'articles': articles,
                                               'category_counter': category_counter,
                                               'tag_counter': tag_counter})