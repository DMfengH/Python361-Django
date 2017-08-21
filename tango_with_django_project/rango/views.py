from django.shortcuts import render
from rango.models import Category
from django.http import HttpResponse
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth .decorators import login_required
from django.contrib.auth import logout

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


def register(request):
    registered = False  # 表示是否注册成功
    if request.method == 'POST':  # 如果有请求
        user_form = UserForm(data=request.POST)  # 从输入处获得信息
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():  # 如果输入信息正确，就进行保存
            user = user_form.save()
            user.set_password(user.password)  # 对密码进行哈希处理，并保存
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:  # 是否上传了图片
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)  # 如果出现错误
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disables.")
        else:
            print("Invalid login details: {0),{1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):   # 登出
    logout(request)
    return HttpResponseRedirect(reverse('index'))