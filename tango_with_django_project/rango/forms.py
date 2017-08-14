from django import forms
from rango.models import Page, Category
# 这个文件是关于数据的格式

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)  # 第一个参数表示不可用户输入，第二个参数表示默认为0
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:  # Meta类有两个用处
        model = Category  # 表示这个form是提供给Category的
        fields = ('name',)  # 表示，包含叫做‘name’的field。只有一个元素的tuple结尾加个逗号，说明这是tuple。


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)
        fields = ('title', 'url', 'views')

    # def clean(self):  # 这个函数用来判断用户输入的url是否正确，进而进行修改。
    #     cleaned_data = self.cleaned_data  # form数据被包含在ModelForm的cleaned_data属性中
    #     url = cleaned_data.get('url')  # 通过get从cleaned_data中获得form的数据
    #
    #     if url and not url.startswith('http://'):
    #         url = 'http://' + url
    #         cleaned_data['url'] = url
    #
    #         return cleaned_data  # 把修改后的数据返回，才会生效。
