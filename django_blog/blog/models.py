from django.db import models
from django.urls import reverse  # 新增这行导入
from django.contrib.auth.models import User  # 导入 Django 内置 User 模型
# 在文件顶部添加
from django.core.validators import FileExtensionValidator

# 1. 先定义 BlogAuthor（必须在 Blog 之前，因为 Blog 要关联它）
# models.py（修改 BlogAuthor 模型，删除冲突字段）
class BlogAuthor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name='blog_author'
    )
    collection_private = models.BooleanField(default=False, verbose_name="Make Collection Private")
    bio = models.TextField(blank=True, verbose_name="Blogger Bio")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Blogger"
        verbose_name_plural = "Blogger"

# 2. 再定义 Category（分类模型）
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    description = models.TextField(blank=True, verbose_name="Category Discription")

    def __str__(self):
        return self.name
    
    # 新增：计算该分类下的博客数量
    def blog_count(self):
        return Blog.objects.filter(category=self, is_published=True).count()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category"

# 图片模型（存储博客内容图片）
class BlogImage(models.Model):
    image = models.ImageField(upload_to='blog_content_images/')  # 上传路径
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"
    
# 3. 定义 Blog（关联 BlogAuthor 和 Category）
class Blog(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(BlogAuthor, on_delete=models.CASCADE, related_name='blogs')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='blogs')  # 分类关联
    description = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    # 封面图（单张）
    cover_image = models.ImageField(
        upload_to='blog_covers/',
        blank=True,
        null=True
    )
    
    # 内容图片（多张，通过 BlogImage 关联）
    content_images = models.ManyToManyField(BlogImage, blank=True, related_name='blogs')
    
    # 视频（单段）
    video = models.FileField(
        upload_to='blog_videos/',
        blank=True,
        null=True
    )

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])

    def __str__(self):
        return self.name
    
# 4. 定义 Collection（收藏模型）
class Collection(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='collections'
    )
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='collections'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="收藏时间")

    class Meta:
        unique_together = ('user', 'blog')  # 避免重复收藏
        verbose_name = "Favorite"
        verbose_name_plural = "Favorite"

    def __str__(self):
        return f"{self.user.username} Favorited 《{self.blog.name}》"

# 5. 评论模型
class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(verbose_name="Comment Content")
    post_date = models.DateTimeField(auto_now_add=True, verbose_name="Comment Time")

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comment"

# 新增模型
from django.db import models
from django.contrib.auth.models import User

class Follow(models.Model):
    follower = models.ForeignKey(
        'BlogAuthor', 
        on_delete=models.CASCADE,
        related_name='following'  # 这次代码不依赖它
    )
    followed = models.ForeignKey(  # 字段名必须是 'followed'，否则上面的代码要改
        'BlogAuthor', 
        on_delete=models.CASCADE,
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

