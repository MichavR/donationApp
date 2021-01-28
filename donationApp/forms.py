from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from donationApp.models import User, Category


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=64, required=True)
    last_name = forms.CharField(max_length=64, required=True)
    email = forms.EmailField(max_length=256, required=True)
    username = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.HiddenInput()
        self.fields['first_name'].widget.attrs.update({'placeholder': ('Imię')})
        self.fields['last_name'].widget.attrs.update({'placeholder': ('Nazwisko')})
        self.fields['email'].widget.attrs.update({'placeholder': ('E-mail')})
        self.fields['password1'].widget.attrs.update({'placeholder': ('Hasło')})
        self.fields['password2'].widget.attrs.update({'placeholder': ('Powtórz hasło')})

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=commit)
        user.set_password(self.cleaned_data["password1"])
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=256)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': ('E-mail')})
        self.fields['password'].widget.attrs.update({'placeholder': ('Hasło')})


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=64, required=True, label="Imię")
    last_name = forms.CharField(max_length=64, required=True, label="Nazwisko")
    email = forms.EmailField(max_length=256, required=True, label="Email")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': ('Imię')})
        self.fields['last_name'].widget.attrs.update({'placeholder': ('Nazwisko')})
        self.fields['email'].widget.attrs.update({'placeholder': ('Email')})


class ExtendedPasswordChangeView(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'placeholder': ('Aktualne hasło')})
        self.fields['new_password1'].widget.attrs.update({'placeholder': ('Nowe hasło')})
        self.fields['new_password2'].widget.attrs.update({'placeholder': ('Powtórz nowe hasło')})

