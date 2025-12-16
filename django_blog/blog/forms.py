# 新增以下全部

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    """扩展Django内置注册表单，增加邮箱字段"""
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # 注册字段：用户名、邮箱、密码1、密码2（确认密码）

from .models import BlogComment

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment  # 关联 BlogComment 模型
        fields = ['description']  # 只需要评论内容字段
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your comment here...'}),
        }
        labels = {
            'description': 'Comment Content',
        }

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Blog, BlogAuthor

class BlogForm(forms.ModelForm):
    """博客表单"""
    class Meta:
        model = Blog
        fields = ['name', 'description', 'is_published']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10}),
        }
        help_texts = {
            'name': 'Enter a title for your blog post',
            'description': 'Write your blog content here',
            'is_published': 'Check this box to make your blog visible to others',
        }

class BlogAuthorForm(forms.ModelForm):
    """博主信息表单"""
    class Meta:
        model = BlogAuthor
        fields = ['bio']  # 明确指定要包含的字段
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5}),
        }

# 用于用户资料（用户名等）编辑的表单
class UserProfileUpdateForm(forms.ModelForm):
    """允许用户编辑个人基本信息的表单"""
    class Meta:
        model = User  # 使用Django内置的User模型
        fields = ['username', 'email', 'first_name', 'last_name']  # 可编辑的字段
        help_texts = {
            'username': '必填。150个字符或更少。字母、数字和@/./+/-/_字符。',
        }