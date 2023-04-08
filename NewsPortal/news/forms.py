from django import forms
from .models import Post, Category, Author
from django.core.exceptions import ValidationError

from .models import Post

class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
           'author',
           'type',
           'title',
           'text',
           'topics',
       ]
       labels={
               'author':'Автор',
               'type':'Тип',
               'title':'Заголовок',
               'text':'Текст',
               'topics':'Категория',
               }
       widgets = {
           'topics': forms.CheckboxSelectMultiple
       }
