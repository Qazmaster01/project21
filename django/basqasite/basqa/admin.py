from django.contrib import admin
from django.utils.safestring import mark_safe

from basqa.models import Basqa, Category





@admin.register(Basqa)
class BasqaAdmin(admin.ModelAdmin):
    # добавляем через админ панель
    fields = ['title', 'slug', 'content', 'photo', 'post_photo', 'cat', 'is_published', 'tags']
    #запретить редактировании
    readonly_fields = ['post_photo']
    prepopulated_fields = {"slug": ("title", )}
    list_display = ('id', 'slug', 'title', 'photo', 'post_photo', 'time_create', 'is_published', 'cat', 'brief_info')
    # кликабельные
    list_display_links = ('title', )
    #sorting
    ordering = ['time_create', 'title']
#     изменить и редактировать статьи
    list_editable = ('is_published', )
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    #панель поиска
    search_fields = ['title__startswith', 'cat__name']
    #фильтр
    list_filter = ['cat__name', 'is_published']

    @admin.display(description='Фото')
    def post_photo(self, basqa: Basqa):
        if basqa.photo:
            return mark_safe(f"<img src='{basqa.photo.url}' width=50>")
        return "Без фото"
    #пользовательский поля
    @admin.display(description='Краткое описанние')
    def brief_info(self, basqa: Basqa):
        return f'Описание {len(basqa.content)} символов'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Basqa.Status.PUBLISHED)

        self.message_user(request, f'Изменено {count} записей.')

    @admin.action(description='Снять выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Basqa.Status.DRAFT)
        self.message_user(request, f'{count} публикации снято с публикации.')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    # кликабельные
    list_display_links = ('id', 'name')


# admin.site.register(Basqa, BasqaAdmin)
