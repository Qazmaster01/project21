from django.urls import path
from . import views
from django.views.decorators.cache import cache_page
urlpatterns = [
    path('', views.BasqaHome.as_view(), name='home'),
    # path('about/', cache_page(60 * 15)((views.about), name='about'),
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.BasqaCategory.as_view(), name='category'),
    path('tag/<slug:tag_post>/', views.show_tag_postlist, name='tag'),
]

