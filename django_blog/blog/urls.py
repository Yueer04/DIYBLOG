from django.urls import path
from . import views

urlpatterns = [
    # 首页（/ 和 /blog/）
    path('', views.IndexView.as_view(), name='index'),
    # 用户注册页面（/blog/register/）
    path('register/', views.UserRegisterView.as_view(), name='register'),
    # 所有博客文章列表（/blog/blogs/）
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    # 热门文章 URL
    path('blogs/popular/', views.PopularBlogListView.as_view(), name='popular-blogs'),
    # 所有博主列表（/blog/bloggers/）
    path('bloggers/', views.BlogAuthorListView.as_view(), name='bloggers'),
    # 博主详细信息页面（/blog/blogger/<author-id>/）
    path('blogger/<int:pk>/', views.BlogListByAuthorView.as_view(), name='blogs-by-author'),
    # 博客帖子详细信息页面（/blog/<blog-id>/）
    path('<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    # 评论表单页面（/blog/<blog-id>/create/）
    path('<int:pk>/create/', views.BlogCommentCreate.as_view(), name='blog-comment-create'),
    # 成为博主的URL
    path('become-blogger/', views.BecomeBloggerView.as_view(), name='become-blogger'),
    path('authors/', views.BlogAuthorListView.as_view(), name='authors'),
    # 博主详情 URL
    path('author/<int:pk>/', views.BlogAuthorDetailView.as_view(), name='blog-author-detail'),
    path('blog/<int:pk>/comment/', views.BlogCommentCreateView.as_view(), name='blog_comment'),
    # 用户个人主页
    path('my-profile/', views.UserProfileView.as_view(), name='user-profile'),
    # 创建博客
    path('blog/create/', views.BlogCreateView.as_view(), name='blog-create'),
    # 更新博客
    path('blog/<int:pk>/update/', views.BlogUpdateView.as_view(), name='blog-update'),
    # 编辑个人简介
    path('edit-bio/', views.EditBioView.as_view(), name='edit-bio'),
    # 用户资料编辑
    path('my-profile/edit/', views.UserProfileUpdateView.as_view(), name='user-profile-update'),
    # 搜索 URL
    path('search/', views.BlogSearchView.as_view(), name='blog-search'),
    # 收藏/取消收藏接口
    path('blog/<int:blog_id>/toggle-collect/', views.toggle_collection, name='toggle-collect'),
    # 我的收藏列表
    path('my-collections/', views.MyCollectionListView.as_view(), name='my-collections'),
    # 博主收藏隐私设置
    path('author/collection-private/', views.set_collection_private, name='set-collection-private'),
    # 关注/取消关注相关
    path('author/<int:author_id>/toggle-follow/', views.toggle_follow, name='toggle-follow'),
    path('author/<int:pk>/follow/', views.FollowAuthorView.as_view(), name='follow-author'),
    path('author/<int:pk>/unfollow/', views.UnfollowAuthorView.as_view(), name='unfollow-author'),
    path('my-following/', views.MyFollowingView.as_view(), name='my-following'),  
    path('my-followers/', views.MyFollowersView.as_view(), name='my-followers'),  
    # 按分类筛选博客的路由
    path('category/<int:category_id>/', views.BlogsByCategoryView.as_view(), name='blogs-by-category'),
    # 新增关注列表和粉丝列表的URL（之前遗漏的）
    path('author/<int:pk>/following/', views.AuthorFollowingView.as_view(), name='author-following'),
    path('author/<int:pk>/followers/', views.AuthorFollowersView.as_view(), name='author-followers'),
]