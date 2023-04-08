from django_filters import FilterSet,DateTimeFilter,CharFilter,ChoiceFilter
from django.forms import DateTimeInput
from .models import Post

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    title= CharFilter(field_name='title',label='Название',lookup_expr='icontains')
    type= ChoiceFilter(field_name='type',label='Тип публикации',empty_label='Все типы',choices=Post.TYPES,)
    time_in= DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Дата публикации после',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        )
    )

    #class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       #model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       #fields = {
           # поиск по названию
           #'title': ['icontains'],
           # количество товаров должно быть больше или равно
           #'type': ['exact'],
           #'time_in': ['date', ],
       #}
