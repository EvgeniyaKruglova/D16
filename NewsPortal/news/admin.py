from django.contrib import admin
from .models import Post, Category, Author, PostCategory
from modeltranslation.admin import TranslationAdmin

class PostCategoryInLine(admin.TabularInline):
    model = PostCategory
    fk_name = 'post'
    extra = 1

def nullfy_quantity(modeladmin, request, queryset):  # все аргументы уже должны быть вам знакомы, самые нужные из них это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(quantity=0)


nullfy_quantity.short_description = 'Обнулить посты'  # описание для более понятного представления в админ панеле задаётся, как будто это объект

class PostAdmin(admin.ModelAdmin):
    inlines = [PostCategoryInLine]
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('author', 'type', 'title')  # оставляем только имя и цену товара
    list_filter = ('author', 'type', 'title')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'text')  # тут всё очень похоже на фильтры из запросов в базу
    actions = [nullfy_quantity]  # добавляем действия в список



# Регистрируем модели для перевода в админке

class CategoryAdmin(TranslationAdmin):
    model = Category


class Post2Admin(TranslationAdmin):
    model = Post

admin.site.register(Category)
#admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
