from django import forms
from .models import Note
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ('title', 'content', 'category', 'chosen', 'ready_to_pub')

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Выберите категорию'

class AuthUserForm(AuthenticationForm, forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class RegisterUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

