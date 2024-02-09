from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from scraping.models import City, Language

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('Данного пользователя не существует.')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Пароль неверный.')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Данный аккаунт недействителен.')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.CharField(label='Введите email',
                            widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Введите пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Введите пароль еще раз',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return data['password2']


class UserUpdateForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=True, to_field_name='slug',
                                  widget=forms.Select(attrs={'class': 'form-control'}), label='Город')
    language = forms.ModelChoiceField(queryset=Language.objects.all(), required=True, to_field_name='slug',
                                      widget=forms.Select(attrs={'class': 'form-control'}), label='Специальность')
    is_send_email = forms.BooleanField(required=False, widget=forms.CheckboxInput, label='Хотите получать рассылку?')

    class Meta:
        model = User
        fields = ('city', 'language', 'is_send_email')

