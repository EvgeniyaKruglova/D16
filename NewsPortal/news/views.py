# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView, View
from .models import Post,Category
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect,get_object_or_404
from django.shortcuts import render
from django.http.response import HttpResponse #импортируем для проверки текста
from django.utils.translation import gettext as _ # импортируем функцию для перевода
from django.utils.translation import activate, get_supported_language_variant

from django.utils import timezone
from django.shortcuts import redirect

import pytz  # импортируем стандартный модуль для работы с часовыми поясами

class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'title'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs
    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        current_time=timezone.localtime(timezone.now())
        context['current_time']=current_time
        context['timezones'] = pytz.common_timezones
        return context
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — .html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'

class PostSearch(ListView):
    model = Post
    # Используем другой шаблон — .html
    template_name = 'search.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'search'
    paginate_by = 10
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs
    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['timezones'] = pytz.common_timezones
        return context
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')

class PostCreate(PermissionRequiredMixin,CreateView):
    # Указываем нашу разработанную форму
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'


class PostUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostDelete(PermissionRequiredMixin,DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.topics = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset= Post.objects.filter (topics=self.topics).order_by('-time_in')
        return queryset

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.topics.subscribers.all()
        context['category']=self.topics
        return context

@login_required
def subscribe(request,pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы успешно подписались на рассылку новостей категории '
    return render(request,'subscribe.html',{'category':category,'message': message})


# class Index (View):
#     def get(self, request):
#
#         current_time = timezone.now()
#         models = Post.objects.all()
#
#         context = {
#             'models': models,
#             'current_time': current_time,
#             'timezones': pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
#         }
#         return HttpResponse(render(request,'index.html', context))
#
#         #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
#
#
#     def post(self, request):
#         request.session['django_timezone'] = request.POST['timezone']
#         return redirect('/')





