from django.shortcuts import render
from rango.models import Category
from django.http import HttpResponse
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm


def index(request):
    # return HttpResponse("Rango sats hey there partner!")  # 返回一句话（HttpResponse是一个要返回的对象）
    category_list = Category.objects.order_by('-likes')[:5]  # 获取Category对象按like的降序排列的前五个
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list,
                    'pages': page_list}  # 这里的categories和HTML中相同，会代替HTML中的。该字典的目的，即将具体信息传递给HTML。

    return render(request, 'rango/index.html', context_dict)  # render()函数将这三个信息综合到一起，然后返回给用户。


def about(request):
    context_dict = {'boldmessage': "a,ab,abo,abou,about!"}
    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}  # 用来render template
    try:
        category = Category.objects.get(slug=category_name_slug)  # 获得category
        pages = Page.objects.filter(category=category)  # 获得对应category下的所有page的列表
        context_dict['pages'] = pages  # 将page以及category添加到context_dict字典中
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    form = CategoryForm()  # 调用forms文件中的CategoryForm

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)
