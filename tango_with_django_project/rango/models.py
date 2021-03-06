from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# 都继承于Django自带的Model base class（django.db.models.Model）
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)  # 设置了几个field，以及相应的类型和属性
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):  # 重新定义了一个save（）函数
        self.slug = slugify(self.name)  # 利用Category的名字产生一个不同的URL
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


# 注意Page与Categories内部的参数不同
class Page(models.Model):
    category = models.ForeignKey(Category)  # ForeignKey是个创建不同model之间一对多关系的一类field【本例中】
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):  # 这句话很有用，没有它，当对对象使用print的时候，结果是<Category: Category object>，不显示名字。
        return self.title
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)   # blank表示这两个可以为空白
    # upload_to的值会和MEDIA_ROOT连在一起作为images的地址
    picture = models.ImageField(upload_to='profile_images', blank=True)
    def __str__(self):
        return self.user.username