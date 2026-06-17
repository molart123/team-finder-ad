import re

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import User


class RegisterForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label='Подтверждение пароля'
    )
    name = forms.CharField(max_length=124, label='Имя')
    surname = forms.CharField(max_length=124, label='Фамилия')

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('password_confirm')
        if password and confirm and password != confirm:
            raise forms.ValidationError('Пароли не совпадают')
        return confirm


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'avatar', 'phone', 'github_url', 'about']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            cleaned = re.sub(r'\D', '', phone)
            if not (
                (phone.startswith('8') and len(cleaned) == 11) or
                (phone.startswith('+7') and len(cleaned) == 11)
            ):
                raise forms.ValidationError(
                    'Телефон должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX'
                )
            # проверка уникальности, исключая себя
            if User.objects.exclude(pk=self.instance.pk).filter(phone=phone).exists():
                raise forms.ValidationError('Этот номер уже используется')
        return phone

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url and not url.startswith('https://github.com/'):
            raise forms.ValidationError('Ссылка должна вести на github.com')
        return url


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Используем стандартный PasswordChangeForm из Django,
    он содержит поля old_password, new_password1, new_password2
    и встроенную валидацию.
    """
    pass