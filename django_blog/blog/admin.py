# 新增以下全部
from django.utils import timezone
# blog/admin.py
from django.contrib import admin
# 导入所有需要的模型，包括新增的 Collection
from .models import Blog, BlogAuthor, BlogComment, Category, Collection, BlogImage  # 导入BlogImage  # 关键：添加 Collection
# 删除
"""
# Minimal registration of Models.
admin.site.register(BlogAuthor)
admin.site.register(BlogComment)
"""

# 新增BlogImage的Admin配置
@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'uploaded_at')
    readonly_fields = ('uploaded_at',)

# 新增 BlogInline
class BlogInline(admin.TabularInline):
    """在作者下方以内联方式显示其撰写的博客"""
    model = Blog
    max_num = 0
    extra = 1
    readonly_fields = ('name', 'post_date', 'is_published') 

# 新增：BlogAuthor 管理配置
@admin.register(BlogAuthor)
class BlogAuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'blog_count', 'collection_private')
    search_fields = ('user__username', 'bio') # 按用户名、简介搜索
    list_filter = ('collection_private',)
    inlines = [BlogInline]
    readonly_fields = []  # 移除 created_at（模型中没有该字段）
    fields = ['user', 'bio', 'collection_private']  # 显示可编辑字段

    # 自定义字段：显示作者的博客数量
    def blog_count(self, obj):
        return obj.blogs.count()
    blog_count.short_description = 'Blog Count' # 列表页字段标题

# 2. 文章内联评论（如果有 BlogComment 模型）
class BlogCommentInline(admin.TabularInline):
    model = BlogComment  # 关联 BlogComment 模型
    readonly_fields = ('description', 'author', 'post_date')
    max_num = 0  # 不允许新增，只显示已有评论

# 修改：Blog 管理配置
# Blog 管理配置
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'post_date', 'is_published', 'comment_count')
    list_editable = ('is_published',)
    list_filter = ('author', 'is_published', 'post_date')
    search_fields = ('name', 'description', 'author__user__username')  # 支持按博客名、内容、作者用户名搜索
    ordering = ('-post_date',)  # 按发布日期降序排列
    list_per_page = 50  # 每页显示50条记录
    fields = [
        ('name', 'author'),
        'category',  # 新增分类字段显示
        'description',
        ('post_date', 'update_date'),
        'is_published',
        'cover_image',  # 新增封面图
        'video',  # 新增视频
        'views'
    ]
    filter_horizontal = ('content_images',)  # 支持在后台选择内容图片
    readonly_fields = ('post_date', 'update_date')  # 日期字段为只读

    # 自定义字段：显示评论数量
    def comment_count(self, obj):
        return obj.blogcomment_set.count()
    comment_count.short_description = 'Comment Count'  # 列表页字段标题

    # 保存模型时的自定义逻辑
    def save_model(self, request, obj, form, change):
        if change:
            obj.update_date = timezone.now()  # 更新时设置更新日期
        else:
            obj.post_date = timezone.now()  # 新建时设置发布日期
            obj.update_date = timezone.now()  # 新建时设置更新日期
        super().save_model(request, obj, form, change)

# 新增：BlogComment 管理配置
@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'author', 'comment_preview', 'post_date')
    list_filter = ['post_date']  # 按发布日期筛选
    search_fields = ('description', 'author__username', 'blog__name')  # 支持按评论内容、作者用户名、博客标题搜索
    ordering = ('-post_date',)  # 按发布日期降序排列
    fields = [
        ('blog', 'author'),  # 所属博客和评论作者（并排显示）
        'description',  # 评论内容
        ('post_date')  # 发布日期
    ]
    readonly_fields = ('post_date',)  # 发布日期为只读
    # 自定义字段：评论内容预览（避免列表页显示过长）
    def comment_preview(self, obj):
        max_length = 50
        if len(obj.description) > max_length:
            return obj.description[:max_length] + '...'
        return obj.description
    comment_preview.short_description = 'Comment'  # 列表页字段标题（英文）

# 新增：注册收藏模型到 Admin
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog', 'created_at']  # 后台列表显示的字段
    list_filter = ['created_at']  # 筛选器：按收藏时间过滤
    search_fields = ['user__username', 'blog__name']  # 搜索框：按用户名、文章名搜索
    readonly_fields = ['created_at']  # created_at 是自动生成的，设为只读（不可编辑）
    date_hierarchy = 'created_at'  # 可选：按时间分层导航