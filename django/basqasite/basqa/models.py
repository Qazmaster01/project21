from captcha.fields import CaptchaField
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
         'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
         'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
         'э': 'e', 'ю': 'yu', 'я': 'ya'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


# отображает только публикованные записи
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Basqa.Status.PUBLISHED)


class Basqa(models.Model):

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Слаг", validators=[
                               MinLengthValidator(5),
                               MaxLengthValidator(100),
                           ])
    photo = models.ImageField(upload_to="photos/%Y/%M/%d/", default=None, blank=True, null=True, verbose_name="Фото")
    content = models.TextField(blank=True, verbose_name="Текст")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата изменении")
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name="Публикация")
    # Связываем форенкей многие к одному строгая одна запись из модель Категории
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts')
    # many-to-many
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True, default=None)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title
    # sorting
    class Meta:
        verbose_name = 'Basqa'
        verbose_name_plural = 'Basqa'
        ordering =['-time_create']
        # чтобы быстрее сортировался
        indexes = [
            models.Index(fields=['time_create'])
        ]
    # ссылка не отображается и мы пропишем специаотный метод и в нем мы будем формировать юрл адрес для каждого адреса с селф
    # отображение по слагам
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    #save data
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit_to_eng(self.title))
    #     super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag-slug': self.slug})

class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')

class Cpacha(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    email = models.EmailField(verbose_name='E-mail')
    content = models.CharField(verbose_name='Контент')