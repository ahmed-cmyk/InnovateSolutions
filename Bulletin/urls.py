from django.urls import path
from . import views
from .views import PostDetailView,CreatePostView

urlpatterns = [
    path('post/new/', CreatePostView.as_view(), name='post_new'),
    path('post/<int:pk>/', PostDetailView, name='post_detail'),
    path('allPosts', views.AllPosts, name='all_posts')

]