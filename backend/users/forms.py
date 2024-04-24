from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from utils.validators import validate_password


class MyUserChangeForm(UserChangeForm):
    new_password = forms.CharField(
        label='Новый пароль', required=False,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = '__all__'

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user
