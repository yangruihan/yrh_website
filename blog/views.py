from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from .models import Article
from .models import Category
from .models import Tag
from django.template.context_processors import request
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ObjectDoesNotExist

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