from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail-post/<str:slug>/', views.detail_post, name='detail-post'),

    path('<slug:slug>/add_comment/', views.add_comment, name='add_comment'),
    path('reply/<int:comment_id>/', views.add_reply, name='add_reply'),
    

    path('like-comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('dislike-comment/<int:comment_id>/', views.dislike_comment, name='dislike_comment'),
    path('like-reply/<int:reply_id>/', views.like_reply, name='like_reply'),
    path('dislike-reply/<int:reply_id>/', views.dislike_reply, name='dislike_reply'),

    path('category_post/<str:slug>/', views.category_post, name='category_post'),
    path('create-post/', views.create_post, name='create-post'),
    path('update-post/<str:slug>/', views.update_post, name='update-post'),
    path('delete-post/<str:slug>/', views.delete_post, name='delete-post'),
]