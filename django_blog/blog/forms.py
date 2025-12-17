from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Blog, BlogAuthor, BlogImage, BlogComment  # 统一导入所有模型

# 1. 用户注册表单
class UserRegisterForm(UserCreationForm):
    """扩展Django内置注册表单，增加邮箱字段"""
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        # 给注册字段添加 form-control 样式
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

# 2. 博客评论表单
class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your comment here...', 'class': 'form-control'}),
        }
        labels = {
            'description': 'Comment Content',
        }

# 3. 博客发布/编辑表单（含媒体上传）
class BlogForm(forms.ModelForm):
    """博客表单（封面图+视频+单张内容图上传）"""
    content_image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*', 'class': 'form-control'}),
        required=False,
        label='Add a Content Image (can add multiple times)'
    )
    
    class Meta:
        model = Blog
        fields = ['name', 'description', 'category', 'is_published', 'cover_image', 'video']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 10, 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    
    def save(self, commit=True):
        blog = super().save(commit=False)
        if commit:
            blog.save()
            # 处理单张内容图片上传
            image = self.cleaned_data.get('content_image')
            if image:
                blog_image = BlogImage.objects.create(image=image)
                blog.content_images.add(blog_image)
        return blog

# 4. 博主信息表单（bio）
class BlogAuthorForm(forms.ModelForm):
    """博主信息表单"""
    class Meta:
        model = BlogAuthor
        fields = ['bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }

# 5. 用户资料编辑表单（核心：解决 add_class 报错）
class UserProfileUpdateForm(forms.ModelForm):
    """允许用户编辑个人基本信息的表单"""
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        help_texts = {
            'username': '必填。150个字符或更少。字母、数字和@/./+/-/_字符。',
        }
        # 关键：添加 widgets 配置，给每个字段加 form-control 类
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

# 6. 冗余表单删除（原文件中的 UserProfileForm 和 BlogAuthorProfileForm 与上面重复，直接删除）