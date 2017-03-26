from django.contrib import admin

from blog_app.models import Post
from blog_app.models import Comment


class PostAdmin(admin.ModelAdmin):
	pass


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
	pass

admin.site.register(Comment, CommentAdmin)

