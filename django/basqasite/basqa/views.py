from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import  render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.views.decorators.cache import cache_page
from .forms import AddPostForm, UploadFileForm, ContactForm
from .models import Basqa, Category, TagPost, UploadFiles, Cpacha

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]

# data_db = [
#     {'id': 1, 'title': 'Цены бензина', 'content': 'Цены', 'is_published': True},
#     {'id': 2, 'title': 'Цены газа', 'content': 'Цены', 'is_published': False},
#     {'id': 3, 'title': 'Цена квартир 2024', 'content': 'Цены', 'is_published': True},
# ]

# def index(request):
#     # передаем посты из таблицы бд а не из db_index
#     posts = Basqa.objects.all().select_related('cat')
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request, 'basqa/index.html', context=data)



# @cache_page(60 * 15)
class BasqaHome(ListView):
    # model = Basqa
    #шаблон
    template_name = 'basqa/index.html'
    # посты и рубрики сайта
    context_object_name = 'posts'
    # статические страницы
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
    }

    def get_queryset(self):
        return Basqa.objects.all().select_related('cat')

    # # передаем посты из таблицы бд а не из db_index
    # # posts = Basqa.objects.all().select_related('cat')
    # template_name = 'basqa/index.html'
    # # extra_context = {
    # #     'title': 'Главная страница',
    # #     'menu': menu,
    # #     'posts': posts,
    # #     'cat_selected': 0,
    # # }
    # #динамическая страница
    # def get_context_data(self, **kwargs):
    #     # передаем посты из таблицы бд а не из db_index
    #     posts = Basqa.objects.all().select_related('cat')
    #
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['posts'] = posts
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context




# def handle_uploaded_file(f):
#     with open(f"uploads/{f.name}", "wb+") as destination:
#         for i in f.chunks():
#             destination.write(i)


#декоратор для доступа только авторизованных пользователей
@login_required
def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(form.cleaned_data['file'])
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'basqa/about.html', {'title': 'О сайте', 'menu': menu, 'form': form})

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             #доавим в бд
#             # try:
#             #     Basqa.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, "Ошибка добавление поста")
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     form = AddPostForm()
#     data = {
#         'menu': menu,
#         'title': 'Добавление статьи',
#         'form': form
#     }
#     return render(request, 'basqa/addpage.html', data)

class AddPage(LoginRequiredMixin, View):
    def get(self, request):
        form = AddPostForm()
        data = {
            'menu': menu,
            'title': 'Добавление статьи',
            'form': form
        }
        return render(request, 'basqa/addpage.html', data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        data = {
            'menu': menu,
            'title': 'Добавление статьи',
            'form': form
        }
        return render(request, 'basqa/addpage.html', data)



class ContactFormView(LoginRequiredMixin, FormView):
    form_class = ContactForm
    template_name = 'basqa/contact.html'
    success_url = reverse_lazy('home')
    title_page = 'Обратная связь'

    def form_valid(self, form):
        if form.is_valid():
            Cpacha.objects.create(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            content=form.cleaned_data['content']
        )
        return super().form_valid(form)


    # def form_valid(self, form):
    #     if form.is_valid():
    #         a = ContactForm(form.cleaned_data)
    #         a.save()


def login(request):
    return HttpResponse('login')

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Basqa.published.filter(cat_id=category.pk).select_related('cat')
    data = {
        'title': f'Рубрика: {category}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'basqa/index.html', context=data)

class BasqaCategory(ListView):
    template_name = 'basqa/index.html'
    context_object_name = 'posts'
    #error 404 pri pustom spicke
    allow_empty = False

    def get_queryset(self):
        return Basqa.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')
# #динамическая страница
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context


# def show_post(request, post_slug):
#     # get_object_or_404 если юрл адрес находит то он перейдет на страницу Бас0а с индексом пк а если нет то генерирует исключение 404
#     post = get_object_or_404(Basqa, slug=post_slug)
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#     return render(request, 'basqa/post.html', data)

class ShowPost(DetailView):
    model = Basqa
    template_name = 'basqa/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Basqa.published, slug=self.kwargs[self.slug_url_kwarg])


def page_not_found(request, exception):
    return HttpResponseNotFound('Страница не найдено')

def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Basqa.Status.PUBLISHED).select_related('cat')

    data = {
        'title': f"Тег: {tag.tag}",
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'basqa/index.html', context=data)
