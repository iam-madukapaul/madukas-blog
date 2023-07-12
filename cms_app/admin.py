from django.contrib import admin
from .models import Post, Category, Comment, Reply


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)} 


admin.site.register(Post, PostAdmin)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at', 'get_likes_count', 'get_dislikes_count', 'status']
    list_filter = ['author', 'created_at', 'status']
    fields = ['author', 'post', 'content', 'status']

    def get_likes_count(self, obj):
        return obj.likes.count()
    get_likes_count.short_description = 'Likes'

    def get_dislikes_count(self, obj):
        return obj.dislikes.count()
    get_dislikes_count.short_description = 'Dislikes'


admin.site.register(Comment, CommentAdmin)


class ReplyAdmin(admin.ModelAdmin):
    list_display = ['author', 'comment', 'created_at', 'get_likes_count', 'get_dislikes_count', 'status']
    list_filter = ['author', 'created_at', 'status']
    fields = ['author', 'comment', 'content', 'status']

    def get_likes_count(self, obj):
        return obj.likes.count()
    get_likes_count.short_description = 'Likes'

    def get_dislikes_count(self, obj):
        return obj.dislikes.count()
    get_dislikes_count.short_description = 'Dislikes'


admin.site.register(Reply, ReplyAdmin)

# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('post', 'name', 'email', 'created_at',)
#     list_filter = ('created_at',)
#     search_fields = ('name', 'email', 'content',)

# admin.site.register(CommentForm, CommentAdmin)

