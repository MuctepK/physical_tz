from django.contrib import admin

from api.models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ['number_of_views']
    list_display = ['id', 'title', 'text', 'created_at']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'created_at']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
