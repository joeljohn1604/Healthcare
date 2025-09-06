from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),  
    path('dashboard/', views.dashboard, name='dashboard'),
    path('blog/create/', views.create_blog_post, name='create_blog_post'),
    path('blog/my-posts/', views.my_blog_posts, name='my_blog_posts'),
    path('blog/', views.blog_posts_by_category, name='blog_list'),
    path('blog/category/<slug:category_slug>/', views.blog_posts_by_category, name='blog_by_category'),
    path('blog/<slug:slug>/', views.blog_post_detail, name='blog_detail'),
]