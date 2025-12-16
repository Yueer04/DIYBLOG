from django.core.management.base import BaseCommand
import random
from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker
from django.db.models import Count
# 修复：导入正确的模型名称（BlogComment 而非 Comment）
from blog.models import BlogAuthor, Blog, Category, Follow, Collection, BlogComment

# 初始化 Faker（英文，避免编码冲突）
fake = Faker('en_US')

# 配置参数（可调整）
NUM_BLOGGERS = 40
NUM_BLOGS = 100
NUM_CATEGORIES = 5
MIN_FOLLOWS = 1
MAX_FOLLOWS = 3
MIN_COLLECTS = 1
MAX_COLLECTS = 3
MIN_COMMENTS = 5  # 每篇博客至少1条评论，避免无评论
MAX_COMMENTS = 10
MIN_VIEWS = 10
MAX_VIEWS = 1000

# 辅助函数：生成随机时间
def random_date(start, end):
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)

class Command(BaseCommand):
    help = 'Generate test data (bloggers, blogs, categories, follows, comments, collections)'

    def handle(self, *args, **options):
        # 解决 Windows 编码问题
        import sys
        sys.stdout.reconfigure(encoding='utf-8')

        # -------------------------- 清空旧数据 --------------------------
        self.stdout.write(self.style.WARNING('⚠️  Clearing old test data...'))
        # 修复：模型名称改为 BlogComment
        Follow.objects.all().delete()
        Collection.objects.all().delete()
        BlogComment.objects.all().delete()  # 正确模型名称
        Blog.objects.all().delete()
        Category.objects.all().delete()
        BlogAuthor.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()
        self.stdout.write(self.style.SUCCESS('✅ Old data cleared!'))

        # -------------------------- 1. 生成分类 --------------------------
        self.stdout.write('\n📚 Generating categories...')
        categories = []
        category_names = [
            "Python Development", "Django Tutorials", "Web Design",
            "Machine Learning", "Database Management"
        ]
        for name in category_names[:NUM_CATEGORIES]:
            category = Category.objects.create(
                name=name,
                description=fake.paragraph(nb_sentences=1)  # 简短描述
            )
            categories.append(category)
        self.stdout.write(self.style.SUCCESS(f'✅ Generated {len(categories)} categories'))

        # -------------------------- 2. 生成博主（含用户账号） --------------------------
        self.stdout.write('\n👥 Generating bloggers...')
        bloggers = []
        for i in range(NUM_BLOGGERS):
            # 生成真实感英文账号信息
            username = fake.user_name()
            email = fake.email()
            first_name = fake.first_name()
            last_name = fake.last_name()

            # 创建 Django User（密码统一为 test123456）
            user = User.objects.create_user(
                username=username,
                email=email,
                password="test123456",
                first_name=first_name,
                last_name=last_name
            )

            # 创建博主资料（BlogAuthor）
            blogger = BlogAuthor.objects.create(
                user=user,
                bio=fake.paragraph(nb_sentences=2),  # 2句话简介
                collection_private=random.choice([True, False])  # 随机隐私设置
            )
            bloggers.append(blogger)

            # 输出博主信息
            self.stdout.write(f'  • Blogger {i+1}: {first_name} {last_name} (username: {username}, email: {email})')

        # -------------------------- 3. 生成关注关系 --------------------------
        self.stdout.write('\n🤝 Generating follow relationships...')
        for blogger in bloggers:
            # 排除自己，随机选择关注对象
            other_bloggers = [b for b in bloggers if b != blogger]
            if not other_bloggers:
                continue

            # 随机关注 1-3 个博主
            num_follows = random.randint(MIN_FOLLOWS, MAX_FOLLOWS)
            followed_bloggers = random.sample(other_bloggers, min(num_follows, len(other_bloggers)))

            # 创建关注记录
            for followed in followed_bloggers:
                Follow.objects.create(
                    follower=blogger,
                    followed=followed,
                    created_at=random_date(timezone.now() - timedelta(days=365), timezone.now())
                )

            # 输出关注统计
            follow_count = blogger.following.count()   # 该博主关注的人数 → 使用 related_name='following'
            follower_count = blogger.followers.count() # 该博主的粉丝数 → 使用 related_name='followers'
            self.stdout.write(f'  • {blogger.user.get_full_name()}: Follows {follow_count} | Has {follower_count} followers')
        # -------------------------- 4. 生成博客 --------------------------
        self.stdout.write('\n📝 Generating blogs...')
        blogs = []
        start_date = timezone.now() - timedelta(days=365)  # 过去一年内的发布时间
        for i in range(NUM_BLOGS):
            # 随机选择作者和分类
            author = random.choice(bloggers)
            category = random.choice(categories)

            # 生成博客内容
            title = fake.sentence(nb_words=5).rstrip('.')  # 5个单词的标题
            content = '\n\n'.join([fake.paragraph(nb_sentences=3) for _ in range(2)])  # 2段内容
            views = random.randint(MIN_VIEWS, MAX_VIEWS)  # 10-1000 随机浏览量
            is_published = True  # 全部设为已发布（避免草稿不显示）

            # 创建博客
            blog = Blog.objects.create(
                name=title,
                author=author,
                category=category,
                description=content,
                post_date=random_date(start_date, timezone.now()),
                update_date=random_date(start_date, timezone.now()),
                is_published=is_published,
                views=views
            )
            blogs.append(blog)

            # 输出博客信息
            self.stdout.write(f'  • Blog {i+1}: "{title}" (Author: {author.user.get_full_name()}, Views: {views})')

        # -------------------------- 5. 生成评论 --------------------------
        self.stdout.write('\n💬 Generating comments...')
        for blog in blogs:
            # 每篇博客生成 1-3 条评论
            num_comments = random.randint(MIN_COMMENTS, MAX_COMMENTS)
            # 随机选择评论者（不能是博客作者）
            commenters = [b for b in bloggers if b != blog.author]
            if not commenters:
                commenters = bloggers  # 极端情况：只有一个博主时自己评论

            selected_commenters = random.sample(commenters, min(num_comments, len(commenters)))

            # 创建评论
            for commenter in selected_commenters:
                comment_content = fake.sentence(nb_words=7)  # 7个单词的评论
                BlogComment.objects.create(
                    blog=blog,
                    author=commenter.user,
                    description=comment_content,
                    post_date=random_date(blog.post_date, timezone.now())  # 评论时间在发布之后
                )

            # 输出评论统计
            comment_count = blog.comments.count()
            self.stdout.write(f'  • "{blog.name[:30]}...": {comment_count} comments')

        # -------------------------- 6. 生成收藏 --------------------------
        self.stdout.write('\n⭐ Generating collections...')
        for blogger in bloggers:
            # 随机收藏 1-3 篇博客（不能是自己的）
            other_blogs = [b for b in blogs if b.author != blogger]
            if not other_blogs:
                continue

            num_collects = random.randint(MIN_COLLECTS, MAX_COLLECTS)
            collected_blogs = random.sample(other_blogs, min(num_collects, len(other_blogs)))

            # 创建收藏记录
            for blog in collected_blogs:
                Collection.objects.create(
                    user=blogger.user,
                    blog=blog,
                    created_at=random_date(blog.post_date, timezone.now())  # 收藏时间在发布之后
                )

            # 输出收藏统计
            collect_count = blogger.user.collections.count()
            self.stdout.write(f'  • {blogger.user.get_full_name()}: Collected {collect_count} blogs')

        # -------------------------- 7. 标记推荐博主（粉丝数前3） --------------------------
        self.stdout.write('\n🏆 Marking recommended bloggers...')
        # 导入 Count 函数（文件顶部要加这个导入）
        from django.db.models import Count
        if BlogAuthor.objects.count() >= 3:
            # 按粉丝数排序，取前3位 → 修复 fake.count 为 Count
            top_authors = BlogAuthor.objects.annotate(
                follower_count=Count('followers')  # 使用 Django ORM 的 Count 统计粉丝数
            ).order_by('-follower_count')[:3]
            self.stdout.write(f'  • Recommended bloggers: {", ".join([a.user.get_full_name() for a in top_authors])}')
        else:
            self.stdout.write('  • Not enough bloggers to mark recommendations')

        # -------------------------- 最终统计 --------------------------
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('🎉 Test data generated successfully!'))
        self.stdout.write('='*60)
        self.stdout.write(f'📊 Summary:')
        self.stdout.write(f'  • Bloggers: {BlogAuthor.objects.count()}')
        self.stdout.write(f'  • Blogs: {Blog.objects.count()}')
        self.stdout.write(f'  • Categories: {Category.objects.count()}')
        self.stdout.write(f'  • Follows: {Follow.objects.count()}')
        self.stdout.write(f'  • Comments: {BlogComment.objects.count()}')
        self.stdout.write(f'  • Collections: {Collection.objects.count()}')
        self.stdout.write('\n💡 Test Account Info:')
        self.stdout.write(f'  • All blogger passwords: test123456')
        self.stdout.write(f'  • Login with any username/email above to test features')
        self.stdout.write('='*60)