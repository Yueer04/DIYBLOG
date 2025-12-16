
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
# blog/views.py 最顶部的导入区域
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView  # 确保包含 ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Blog, BlogAuthor, Category, BlogComment, Follow, Collection  # 确保所有模型都导入
from .forms import BlogCommentForm  # 如有表单，也需导入

from django.views import generic
from .models import Blog, BlogAuthor, BlogComment
from django.contrib.auth.models import User #Blog author or commenter

from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogAuthor, BlogComment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate  # 用于自动登录
from .forms import UserRegisterForm, BlogCommentForm  # 导入表单
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView

# 新增：用户注册视图
# 将原UserRegisterView的success_url修改为登录页
class UserRegisterView(generic.CreateView):
    form_class = UserRegisterForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')  # 注册成功后跳转登录页

    def form_valid(self, form):
        """表单验证通过后，创建用户但不自动登录"""
        # 只保存用户，不自动登录
        form.save()
        return super().form_valid(form)

from .models import Blog, BlogAuthor, BlogComment, Category  # 确保导入Category

def index(request):
    """首页视图：添加分类数据"""
    latest_blogs = Blog.objects.filter(is_published=True).order_by('-post_date')[:5]
    popular_blogs = Blog.objects.filter(is_published=True).order_by('-views')[:5]
    categories = Category.objects.all()  # 获取所有分类
    top_authors = BlogAuthor.objects.annotate(
        follower_count=models.Count('followers')
    ).order_by('-follower_count')[:3]  # 推荐博主

    return render(
        request,
        'index.html',
        {
            'latest_blogs': latest_blogs,
            'popular_blogs': popular_blogs,
            'categories': categories,  # 传递分类到模板
            'top_authors': top_authors
        }
    )

# 修正 BlogListView 以匹配要求
class BlogListView(generic.ListView):
    """
    Generic class-based view for a list of all blogs.
    """
    model = Blog
    paginate_by = 5
    template_name = 'blog/blog_list.html'  # 明确指定模板
    context_object_name = 'blog_list'  # 确保模板使用正确的变量名

    def get_queryset(self):
        # 只显示已发布的博客，按发布日期倒序
        return Blog.objects.filter(is_published=True).order_by('-post_date')

# 新增：所有博主列表视图
class BlogAuthorListView(generic.ListView):
    model = BlogAuthor
    template_name = 'blog/blogauthor_list.html'
    context_object_name = 'blogger_list'
    queryset = BlogAuthor.objects.all().order_by('user__username')
    paginate_by = 10  # 分页（10位博主一页）

class BlogListByAuthorView(generic.ListView):
    """
    Generic class-based view for a list of blogs posted by a particular BlogAuthor.
    """
    model = Blog
    paginate_by = 5
    context_object_name = 'blogs'
    template_name ='blog/blog_list_by_author.html'
    
    # 修改
    def get_queryset(self):
        id = self.kwargs['pk']
        target_author = get_object_or_404(BlogAuthor, pk=id)
        # 只显示已发布的博客
        return Blog.objects.filter(author=target_author, is_published=True).order_by('-post_date')
    
    # 移除分页
    paginate_by 
    def get_context_data(self, **kwargs):
        """
        Add BlogAuthor to context so they can be displayed in the template
        """
        # Call the base implementation first to get a context
        context = super(BlogListByAuthorView, self).get_context_data(**kwargs)
        # Get the blogger object from the "pk" URL parameter and add it to the context
        context['blogger'] = get_object_or_404(BlogAuthor, pk = self.kwargs['pk'])
        return context
    
    

class BloggerListView(generic.ListView):
    """
    Generic class-based view for a list of bloggers.
    """
    model = BlogAuthor
    paginate_by = 5


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse


class BlogCommentCreate(LoginRequiredMixin, CreateView):
    """
    Form for adding a blog comment. Requires login. 
    """
    # 修改
    model = BlogComment
    template_name = 'blog/blogcomment_form.html'
    fields = ['description']  # 仅显示评论内容字段（其他字段自动填充）
    login_url = '/accounts/login/'  # 未登录重定向到登录页

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super(BlogCommentCreate, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['blog'] = get_object_or_404(Blog, pk = self.kwargs['pk'])
        return context
        
    def form_valid(self, form):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        """
        #Add logged-in user as author of comment
        form.instance.author = self.request.user
        #Associate comment with blog based on passed id
        form.instance.blog=get_object_or_404(Blog, pk = self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super(BlogCommentCreate, self).form_valid(form)

    def get_success_url(self): 
        """
        After posting comment return to associated blog.
        """
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk'],})

# 新增：评论创建视图（必须登录才能访问）
class BlogCommentCreateView(LoginRequiredMixin, CreateView):
    model = BlogComment
    form_class = BlogCommentForm
    template_name = 'blog/blog_comment_form.html'  # 评论表单模板

    def form_valid(self, form):
        # 关联当前博客和评论者（登录用户）
        form.instance.blog = Blog.objects.get(pk=self.kwargs['pk'])  # 从URL获取博客ID
        form.instance.author = self.request.user  # 评论者是当前登录用户
        form.instance.is_approved = True  # 自动批准评论（也可设置为False，需要管理员审核）
        return super().form_valid(form)

    def get_success_url(self):
        # 评论提交成功后，跳转回原博客详情页
        return reverse_lazy('blog-detail', kwargs={'pk': self.kwargs['pk']})
    
# 新增“成为博主”视图（需放在文件末尾）
class BecomeBloggerView(LoginRequiredMixin, CreateView):
    """让已登录用户创建博主资料"""
    model = BlogAuthor
    fields = ['bio']  # 仅需填写个人简介
    template_name = 'blog/become_blogger.html'
    success_url = reverse_lazy('index')  # 成功后跳首页
    login_url = '/accounts/login/'  # 未登录则跳转登录页

    def form_valid(self, form):
        # 将当前登录用户与博主资料关联
        form.instance.user = self.request.user
        return super().form_valid(form)
    
# 新增：博主详情视图
class BlogAuthorDetailView(DetailView):
    model = BlogAuthor
    context_object_name = 'blog_author'
    template_name = 'blog/blogauthor_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(** kwargs)
        # 获取博主的博客
        context['author_blogs'] = self.object.blogs.filter(is_published=True).order_by('-post_date')
        # 获取关注数和粉丝数
        context['following_count'] = self.object.following.count()
        context['followers_count'] = self.object.followers.count()
        # 检查当前用户是否已关注该博主
        if self.request.user.is_authenticated and hasattr(self.request.user, 'blogauthor'):
            context['is_following'] = self.object.followers.filter(
                id=self.request.user.blogauthor.id
            ).exists()
        return context
    
# 新增导入
from django.views.generic.edit import UpdateView, DeleteView
from .forms import BlogForm, BlogAuthorForm

# 新增用户个人主页视图
class UserProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'blog/user_profile.html'
    login_url = '/accounts/login/'

    def get_context_data(self,** kwargs):
        context = super().get_context_data(**kwargs)
        # 获取当前用户
        user = self.request.user
        # 检查用户是否是博主
        try:
            blog_author = BlogAuthor.objects.get(user=user)
            context['blog_author'] = blog_author
            # 获取该博主的所有博客（包括未发布的）
            context['my_blogs'] = Blog.objects.filter(author=blog_author).order_by('-post_date')
        except BlogAuthor.DoesNotExist:
            context['blog_author'] = None
            context['my_blogs'] = []
        return context

# 新增博客创建视图
class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    login_url = '/accounts/login/'

    def form_valid(self, form):
        # 设置当前用户为博客作者（需先成为博主）
        try:
            form.instance.author = BlogAuthor.objects.get(user=self.request.user)
            return super().form_valid(form)
        except BlogAuthor.DoesNotExist:
            # 如果用户不是博主，重定向到成为博主页面
            return redirect('become-blogger')

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'pk': self.object.pk})

# 新增博客更新视图
class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    login_url = '/accounts/login/'

    def get_queryset(self):
        # 确保用户只能编辑自己的博客
        return Blog.objects.filter(author__user=self.request.user)

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'pk': self.object.pk})

# 新增编辑个人简介视图
class EditBioView(LoginRequiredMixin, UpdateView):
    model = BlogAuthor
    form_class = BlogAuthorForm  # 表单已定义包含的字段
    template_name = 'blog/edit_bio.html'
    login_url = '/accounts/login/'
    success_url = reverse_lazy('user-profile')

    def get_object(self, queryset=None):
        return BlogAuthor.objects.get(user=self.request.user)

from .forms import UserRegisterForm, UserProfileUpdateForm  # 补充导入新表单
#新增
class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    允许用户编辑自己的基本信息（用户名、邮箱等）
    """
    model = User
    form_class = UserProfileUpdateForm
    template_name = 'blog/user_profile_update.html'
    login_url = '/accounts/login/'
    success_url = reverse_lazy('user-profile')

    def get_object(self, queryset=None):
        """确保用户只能编辑自己的信息"""
        return self.request.user
    
# 修改 BlogSearchView
from django.db.models import Q  # 导入 Q 对象
from django.views import generic
from .models import Blog

# 新增
# blog/views.py 中的 BlogSearchView 类
class BlogSearchView(ListView):
    model = Blog
    template_name = 'blog/blog_search.html'  # 确保有对应的模板文件
    context_object_name = 'blog_list'
    paginate_by = 10  # 可选：分页，每页10篇博客

    def get_queryset(self):
        # 获取搜索关键词
        query = self.request.GET.get('q', '')
        # 搜索博客标题和内容（包含关键词）
        if query:
            return Blog.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query),
                is_published=True  # 只搜索已发布的博客
            ).order_by('-post_date')
        # 无关键词时返回空列表或所有博客
        return Blog.objects.filter(is_published=True).order_by('-post_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(** kwargs)
        # 传递搜索关键词到模板（用于显示搜索结果提示）
        context['search_query'] = self.request.GET.get('q', '')
        return context

from django.views import generic
from django.db.models import Count
from .models import Blog, BlogAuthor, Category  # 分类模型是 Category


# 新增热门文章列表视图
class PopularBlogListView(generic.ListView):
    model = Blog
    template_name = 'blog/blog_list.html'  # 可以复用已有的文章列表模板
    context_object_name = 'blog_list'
    paginate_by = 10  # 分页，每页显示10篇

    def get_queryset(self):
        # 按阅读量倒序排列（已发布的文章）
        return Blog.objects.filter(is_published=True).order_by('-views')
    
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Blog, Collection, BlogAuthor, Follow

# 1. 收藏/取消收藏接口（AJAX 异步请求，无刷新操作）
@login_required  # 必须登录才能收藏
def toggle_collection(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, is_published=True)
    # 检查用户是否已收藏该文章
    collection, created = Collection.objects.get_or_create(
        user=request.user,
        blog=blog
    )
    if not created:
        # 已收藏 → 取消收藏（删除记录）
        collection.delete()
        return JsonResponse({
            'status': 'success',
            'action': 'uncollect',
            'collection_count': blog.collections.count()  # 更新后的收藏数
        })
    else:
        # 未收藏 → 新增收藏
        return JsonResponse({
            'status': 'success',
            'action': 'collect',
            'collection_count': blog.collections.count()
        })

# 2. 我的收藏列表（个人中心 - 登录后才能访问）
class MyCollectionListView(LoginRequiredMixin, generic.ListView):
    model = Collection
    template_name = 'blog/my_collections.html'
    context_object_name = 'collections'
    login_url = '/accounts/login/'

    def get_queryset(self):
        # 查询当前用户的所有收藏，并关联博客信息
        return Collection.objects.filter(
            user=self.request.user
        ).select_related('blog', 'blog__author').order_by('-created_at')\
        
# 3. 优化 BlogDetailView（文章详情页，显示收藏数和收藏状态）
class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get_object(self, queryset=None):
        # 阅读量+1 逻辑
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
        # 收藏功能相关上下文
        context['collection_count'] = blog.collections.count()
        context['is_collected'] = Collection.objects.filter(
            user=self.request.user, blog=blog
        ).exists()
        # 评论功能上下文（如果有）
        context['comments'] = blog.comments.all().order_by('-post_date')
        context['comment_form'] = BlogCommentForm()  # 评论表单
        return context

# 4. 优化 IndexView/ BlogListView（首页/文章列表页，显示收藏数）
from django.views.generic import ListView
from .models import Blog

class IndexView(ListView):
    model = Blog
    template_name = 'blog/index.html'
    context_object_name = 'blog_list'
    paginate_by = 10  # 可选：首页博客列表分页（每页10篇）

    def get_context_data(self, **kwargs):
        context = super().get_context_data(** kwargs)
        
        # 1. 传递「最新文章」变量（latest_blogs）：最近发布的5篇已发布博客
        context['latest_blogs'] = Blog.objects.filter(
            is_published=True  # 只显示已发布的
        ).order_by('-post_date')[:5]  # 按发布时间倒序，取前5篇

        # 2. 传递「热门文章」变量（popular_blogs）：浏览量最高的5篇已发布博客
        context['popular_blogs'] = Blog.objects.filter(
            is_published=True
        ).order_by('-views')[:5]  # 按浏览量倒序，取前5篇

        # 3. 之前添加的「收藏数」计算逻辑（保留）
        for blog in context['blog_list']:
            blog.collection_count = blog.collections.count()

        return context
    
@login_required
def set_collection_private(request):
    if request.method == 'POST':
        # 获取当前用户的 BlogAuthor 实例（如果是博主）
        try:
            blog_author = request.user.blogauthor
        except BlogAuthor.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '仅博主可设置收藏隐私'})
        
        # 更新隐私设置（POST 数据中的 'collection_private' 是字符串 'true'/'false'）
        is_private = request.POST.get('collection_private') == 'true'
        blog_author.collection_private = is_private
        blog_author.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': '仅支持 POST 请求'})

@login_required
def toggle_follow(request, author_id):
    """关注/取消关注博主"""
    author = get_object_or_404(BlogAuthor, id=author_id)
    
    # 检查是否已关注
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        followed=author
    )
    
    # 如果已关注则取消关注
    if not created:
        follow.delete()
    
    # 返回到博主详情页
    return redirect('blog-author-detail', pk=author_id)

# 新增
class MyFollowingView(LoginRequiredMixin, generic.ListView):
    """查看当前用户关注的博主列表"""
    model = Follow
    template_name = 'blog/my_following.html'
    context_object_name = 'following_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user).select_related('followed')


class MyFollowersView(LoginRequiredMixin, generic.ListView):
    """查看当前用户的粉丝列表"""
    model = Follow
    template_name = 'blog/my_followers.html'
    context_object_name = 'followers_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        # 获取当前用户的博主资料
        blog_author = get_object_or_404(BlogAuthor, user=self.request.user)
        return Follow.objects.filter(followed=blog_author).select_related('follower')
    
# 新增以下视图
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import BlogAuthor

class FollowAuthorView(LoginRequiredMixin, generic.View):
    """关注博主视图"""
    login_url = '/accounts/login/'

    def post(self, request, *args, **kwargs):
        # 获取当前登录用户的博主身份（必须是博主才能关注他人）
        try:
            current_author = BlogAuthor.objects.get(user=request.user)
        except BlogAuthor.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '请先成为博主才能关注他人'}, status=400)
        
        # 获取要关注的目标博主
        target_author = get_object_or_404(BlogAuthor, pk=kwargs['pk'])
        
        # 避免自己关注自己
        if current_author == target_author:
            return JsonResponse({'status': 'error', 'message': '不能关注自己'}, status=400)
        
        # 添加关注关系
        current_author.following.add(target_author)
        return JsonResponse({'status': 'success', 'message': '关注成功'})

class UnfollowAuthorView(LoginRequiredMixin, generic.View):
    """取消关注博主视图"""
    login_url = '/accounts/login/'

    def post(self, request, *args, **kwargs):
        try:
            current_author = BlogAuthor.objects.get(user=request.user)
        except BlogAuthor.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '请先成为博主'}, status=400)
        
        target_author = get_object_or_404(BlogAuthor, pk=kwargs['pk'])
        
        # 取消关注
        current_author.following.remove(target_author)
        return JsonResponse({'status': 'success', 'message': '取消关注成功'})
    
# 新增我的关注视图
class MyFollowingView(LoginRequiredMixin, generic.ListView):
    model = Follow
    template_name = 'blog/my_following.html'
    context_object_name = 'following_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        # 获取当前用户的博主资料
        blog_author = get_object_or_404(BlogAuthor, user=self.request.user)
        # 查询当前博主关注的所有博主（通过followed字段）
        return [follow.followed for follow in Follow.objects.filter(follower=blog_author)]


# 新增我的粉丝视图
class MyFollowersView(LoginRequiredMixin, generic.ListView):
    model = Follow
    template_name = 'blog/my_followers.html'
    context_object_name = 'followers_list'
    login_url = '/accounts/login/'

    def get_queryset(self):
        # 获取当前用户的博主资料
        blog_author = get_object_or_404(BlogAuthor, user=self.request.user)
        # 查询关注当前博主的所有粉丝（通过follower字段）
        return [follow.follower for follow in Follow.objects.filter(followed=blog_author)]
    
from django.views.generic import ListView
from .models import Blog, Category

# 按分类筛选博客的视图
class BlogsByCategoryView(ListView):
    model = Blog
    template_name = 'blog/blogs_by_category.html'
    context_object_name = 'blog_list'

    def get_queryset(self):
        # 原有逻辑：根据分类ID筛选博客
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        return Blog.objects.filter(category=self.category).order_by('-post_date')

    # 新增/修改 get_context_data 方法
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 给当前分类下的所有博客，添加 collection_count（收藏数）
        blog_list = context['blog_list']  # 对应上面的 context_object_name
        for blog in blog_list:
            blog.collection_count = blog.collections.count()  # 计算该博客的收藏数
        # 保留原有分类信息传递（如果之前有的话）
        context['category'] = self.category
        return context
    
# 博主的关注列表
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.db.models import F  # 导入 F 表达式
from .models import BlogAuthor, Follow

class AuthorFollowingView(ListView):
    template_name = 'blog/author_following.html'
    context_object_name = 'following_list'
    paginate_by = 10

    def get_queryset(self):
        # 1. 获取当前博主（从URL参数提取ID）
        blog_author_id = self.kwargs.get('pk')
        self.blog_author = get_object_or_404(BlogAuthor, pk=blog_author_id)
        
        # 2. 关键修复：先查询 Follow 记录，再提取其中的 'followed' 字段（即被关注的 BlogAuthor）
        # values_list('followed', flat=True) → 提取所有被关注博主的ID列表
        # BlogAuthor.objects.filter(pk__in=...) → 根据ID列表查询 BlogAuthor 实例
        followed_ids = Follow.objects.filter(
            follower=self.blog_author  # 筛选当前博主发起的关注
        ).values_list('followed', flat=True)  # 只取被关注者的ID
        
        # 3. 返回 BlogAuthor 实例列表（模板需要的类型）
        return BlogAuthor.objects.filter(pk__in=followed_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(** kwargs)
        context['blog_author'] = self.blog_author  # 传递当前博主信息到模板
        return context

class AuthorFollowersView(ListView):
    template_name = 'blog/author_followers.html'
    context_object_name = 'followers_list'  # 模板中接收的变量名
    paginate_by = 10  # 可选：分页，每页10个粉丝

    def get_queryset(self):
        # 1. 获取当前博主（从URL参数提取ID）
        blog_author_id = self.kwargs.get('pk')
        self.blog_author = get_object_or_404(BlogAuthor, pk=blog_author_id)
        
        # 2. 关键：查询所有关注当前博主的 Follow 记录，提取「关注者」（follower 字段）
        # 粉丝 = 所有将当前博主设为「被关注者」的用户
        follower_ids = Follow.objects.filter(
            followed=self.blog_author  # 筛选「被关注者」是当前博主的记录
        ).values_list('follower', flat=True)  # 提取「关注者」的ID列表
        
        # 3. 根据ID列表查询 BlogAuthor 实例（模板需要的类型）
        return BlogAuthor.objects.filter(pk__in=follower_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(** kwargs)
        context['blog_author'] = self.blog_author  # 传递当前博主信息到模板
        return context