"""
URL configuration for diyblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# 新增include导入
from django.urls import path, include
# 新增RedirectView导入
from django.views.generic import RedirectView
# 新增静态文件设置导入
from django.conf import settings
# 新增静态文件URL映射导入
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # 新增：包含博客应用的URL配置
    path('blog/', include('blog.urls')), 
    # 新增：将根URL重定向到博客首页
    path('', RedirectView.as_view(url='/blog/', permanent=True)),
    # 添加认证相关URL
    path('accounts/', include('django.contrib.auth.urls')),  # 新增这一行
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # 新增：配置媒体文件的URL映射