from django import forms

from django.contrib.auth.models import User 

from blog_app.models import Post
from blog_app.models import Comment

class PostForm(forms.ModelForm):
	class Meta():
		model = Post
		fields = (
		    'title',
		    'body',	
		)


class CommentForm(forms.ModelForm):
	class Meta():
		model = Comment
		fields = (
		    'author',
		    'text',
		)


class UserForm(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput())
	username = forms.CharField()

	class Meta():
		model = User
		fields = (
			'username', 
			'password',
		)

	need_valid_user = False
