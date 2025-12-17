# DIY Blog - 基于Django的博客平台

DIY Blog是一个使用Django框架开发的简易博客平台，允许用户注册账号、发布博客文章、添加评论、关注博主以及收藏喜欢的文章。

## 功能特点

- **用户系统**：注册、登录、个人资料管理
- **博客功能**：发布、编辑、查看博客文章，支持分类管理
- **互动功能**：评论、关注博主、收藏文章
- **媒体支持**：上传博客封面图、内容图片和视频
- **内容发现**：按分类筛选、热门文章推荐、推荐博主

## 技术栈

- 后端：Python 3.x + Django 6.0
- 前端：HTML + CSS + Bootstrap 5
- 数据库：SQLite（开发环境）
- 其他：Faker（测试数据生成）

## 项目结构

```
django_blog/                  # 项目根目录
├── db.sqlite3                # SQLite数据库文件
├── manage.py                 # Django命令行工具
├── diyblog/                  # 项目主配置包
│   ├── __init__.py           # 包初始化文件
│   ├── asgi.py               # ASGI配置（异步部署）
│   ├── settings.py           # 项目设置（数据库、应用等配置）
│   ├── urls.py               # 主URL配置
│   └── wsgi.py               # WSGI配置（同步部署）
├── blog/                     # 博客应用
│   ├── __init__.py           # 包初始化文件
│   ├── admin.py              # 后台管理配置
│   ├── apps.py               # 应用配置
│   ├── forms.py              # 表单定义（评论表单等）
│   ├── models.py             # 数据模型（博客、用户、评论等）
│   ├── views.py              # 视图逻辑（页面渲染、数据处理）
│   ├── urls.py               # 应用URL路由配置
│   ├── migrations/           # 数据库迁移文件目录
│   │   └── __init__.py
│   ├── templates/            # 模板文件目录
│   │   ├── blog/             # 博客应用模板
│   │   │   ├── index.html    # 首页模板
│   │   │   ├── blog_list.html # 博客列表模板
│   │   │   ├── blog_detail.html # 博客详情模板
│   │   │   ├── blogcomment_form.html # 评论表单模板
│   │   │   ├── register.html # 用户注册模板
│   │   │   ├── user_profile.html # 用户个人主页模板
│   │   │   ├── blogauthor_list.html # 博主列表模板
│   │   │   ├── blogauthor_detail.html # 博主详情模板
│   │   │   ├── become_blogger.html # 成为博主申请模板
│   │   │   ├── user_profile_update.html # 用户资料编辑模板
│   │   │   ├── edit_bio.html # 个人简介编辑模板
│   │   │   ├── blog_search.html # 博客搜索结果模板
│   │   │   ├── author_following.html # 博主关注列表模板
│   │   │   ├── author_followers.html # 博主粉丝列表模板
│   │   │   ├── my_collections.html # 我的收藏列表模板
│   │   │   ├── blog_create.html # 创建博客模板
│   │   │   ├── blog_update.html # 更新博客模板
│   │   │   └── blogs_by_category.html # 按分类筛选博客模板
│   │   └── registration/     # 认证相关模板
│   │       ├── password_reset_complete.html # 密码重置完成模板
│   │       ├── password_reset_done.html # 密码重置邮件发送完成模板
│   │       ├── login.html    # 登录模板
│   │       ├── password_reset_form.html # 密码重置表单模板
│   │       └── password_reset_confirm.html # 密码重置确认模板
│   ├── management/           # 自定义管理命令目录
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── generate_test_data.py # 生成测试数据命令
│   └── static/               # 应用内静态文件（可选）
│       └── blog/             # 应用专属静态资源
│           ├── css/
│           ├── js/
│           └── images/
├── static/                   # 项目级静态文件目录（CSS、JS、图片等）
│   ├── css/                  # 样式表
│   ├── js/                   # JavaScript文件
│   └── images/               # 图片资源（如default-avatar.png）
├── media/                    # 用户上传文件目录
│   ├── blog_covers/          # 博客封面图
│   ├── blog_content_images/  # 博客内容图片
│   └── blog_videos/          # 博客视频
```

## 快速开始

### 前提条件

- Python 3.8+（推荐3.10+）
- pip（Python包管理器，通常随Python安装）
- 网络连接（用于安装依赖包）

### 安装步骤

1. **获取项目代码**  
   假设您已获取项目源代码（通过克隆仓库或下载压缩包），进入项目根目录：
   ```bash
   # 若使用Git克隆
   git clone <仓库地址>
   cd django_blog
   ```

2. **创建并激活虚拟环境**  
   虚拟环境可隔离项目依赖，避免与系统Python环境冲突：
   ```bash
   # 创建虚拟环境
   python -m venv venv

   # 激活虚拟环境
   # Windows系统（命令提示符）
   venv\Scripts\activate
   # Windows系统（PowerShell）
   .\venv\Scripts\Activate.ps1
   # macOS/Linux系统
   source venv/bin/activate
   ```
   激活成功后，终端提示符前会显示`(venv)`

3. **安装依赖包**  
   项目依赖已在代码中体现，执行以下命令安装：
   ```bash
   pip install django faker
   ```
   （可选）验证安装：
   ```bash
   pip list | grep django  # 应显示django==6.0.x
   pip list | grep faker   # 应显示faker==x.x.x
   ```

4. **初始化数据库**  
   Django使用迁移文件管理数据库结构，执行以下命令创建初始数据库：
   ```bash
   # 生成迁移文件（根据models.py创建数据库表结构）
   python manage.py makemigrations

   # 应用迁移（创建数据库表）
   python manage.py migrate
   ```
   执行成功后，项目根目录会生成`db.sqlite3`文件

5. **创建超级管理员**  
   超级管理员可访问Django后台管理系统，执行以下命令并按提示设置账号密码：
   ```bash
   python manage.py createsuperuser
   ```
   示例：
   ```
   Username: admin
   Email address: admin@example.com
   Password: （输入密码，输入时不显示）
   Password (again): （再次输入密码）
   Superuser created successfully.
   ```

6. **生成测试数据（可选）**  
   若需要测试数据快速体验功能，执行自定义命令：
   ```bash
   python manage.py generate_test_data
   ```
   该命令会创建：
   - 随机测试用户（密码统一为`test123456`）
   - 博客文章、分类、评论
   - 关注关系和收藏数据

7. **启动开发服务器**  
   运行以下命令启动本地开发服务器：
   ```bash
   python manage.py runserver
   ```
   成功后会显示：
   ```
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CONTROL-C.
   ```

8. **访问网站**  
   打开浏览器，访问以下地址：
   - 网站首页：http://127.0.0.1:8000/
   - 管理后台：http://127.0.0.1:8000/admin/（使用超级管理员账号登录）

### 停止服务

- 在终端按 `Ctrl+C` 停止开发服务器
- 退出虚拟环境：
  ```bash
  deactivate
  ```

## 使用指南

### 普通用户操作

1. **注册账号**  
   - 点击首页右上角"Signup"链接
   - 填写用户名、邮箱、密码（密码需包含字母和数字，长度≥8位）
   - 注册成功后自动跳转至登录页

2. **登录系统**  
   - 点击首页右上角"Login"链接
   - 输入用户名和密码登录
   - 登录后可使用评论、关注、收藏等功能

3. **浏览内容**  
   - 首页展示最新文章和热门推荐
   - 点击文章标题查看详情
   - 通过右侧分类导航筛选感兴趣的内容

4. **互动功能**  
   - **评论**：在文章详情页底部点击"Add a new comment"提交评论
   - **关注博主**：在博主详情页点击"Follow"按钮
   - **收藏文章**：在文章详情页点击收藏按钮（星形图标）

### 博主功能

1. **成为博主**  
   - 登录后点击导航栏"Become blogger"
   - 填写个人简介并提交，即可获得发布文章权限

2. **发布博客**  
   - 点击个人主页的"+ 发布文章"按钮
   - 填写标题、内容，选择分类
   - 可选：上传封面图、内容图片或视频
   - 点击"发布"按钮（可选择"保存草稿"稍后发布）

3. **管理文章**  
   - 在个人主页可查看所有自己发布的文章
   - 点击"编辑"按钮修改文章内容
   - 点击"删除"按钮移除不需要的文章

4. **个人资料管理**  
   - 点击"编辑资料"修改个人信息
   - 可更新用户名、邮箱、个人简介等

## 后台管理功能

1. **登录后台**  
   访问 http://127.0.0.1:8000/admin/，使用超级管理员账号登录

2. **核心管理功能**  
   - **用户管理**：查看/创建/删除用户，修改用户权限
   - **内容管理**：审核博客文章、评论，管理分类
   - **媒体管理**：查看用户上传的图片和视频
   - **数据统计**：查看各模型数据量统计

3. **常用操作**  
   - 审核未通过的评论：在"Comments"列表中勾选并选择"Approve"
   - 批量删除垃圾内容：勾选目标内容，选择"Delete selected"
   - 导出数据：部分模型支持CSV/JSON格式导出

## 常见问题

1. **忘记超级管理员密码？**  
   执行以下命令重置：
   ```bash
   python manage.py changepassword admin  # admin为用户名
   ```

2. **上传文件失败？**  
   - 检查文件大小是否超过50MB限制（配置在`settings.py`）
   - 确保媒体文件格式符合要求（图片支持jpg/png，视频支持mp4等）

3. **页面样式错乱？**  
   收集静态文件：
   ```bash
   python manage.py collectstatic
   ```

## 致谢

- [Django](https://www.djangoproject.com/) - 强大的Python Web框架
- [Bootstrap](https://getbootstrap.com/) - 前端UI框架
- [Faker](https://faker.readthedocs.io/) - 测试数据生成工具
- [Bootstrap Icons](https://icons.getbootstrap.com/) - 图标库
