from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator

from .models import Category, Basqa


# енеобязателен для формы в хтил виде
class AddPostForm(forms.ModelForm):
    # title = forms.CharField(max_length=255, label='Зоголовок', min_length=5, widget=forms.TextInput(attrs={'class': 'form-input'}))
    # slug = forms.SlugField(max_length=255, label='URL',
    #                        validators=[
    #                            MinLengthValidator(5),
    #                            MaxLengthValidator(100),
    #                        ])
    # content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Контент')
    # is_published = forms.BooleanField(required=False, initial=False, label='Публикация')
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label='Категория не выбрана', label='Категория')

    # формирование двух таблиц моделей
    class Meta:
        model = Basqa
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-imput'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {'slug': 'URL'}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')

        return title

class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Файл")


class ContactForm(forms.Form):
    name = forms.CharField(label='Название', max_length=255)
    email = forms.EmailField(label='E-mail')
    content = forms.CharField(label='Контент', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()