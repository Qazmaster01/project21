from django import template
import basqa.views as views
from basqa.models import Category, TagPost

register = template.Library()


# @register.simple_tag(name='getcats')
# def get_categories():
#     return views.cats_db

@register.simple_tag
def get_menu():
    return views.menu

@register.inclusion_tag('basqa/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('basqa/list_tags.html')
def show_all_tags():
    return {'tags': TagPost.objects.all()}