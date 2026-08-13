from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class AdminUserCreationForm(UserCreationForm):
    is_staff_user = forms.BooleanField(
        required=False, 
        label="منحه صلاحيات الأدمن (Admin)",
        widget=forms.CheckboxInput(attrs={'style': 'margin-right: 10px;'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff_user']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('is_staff_user'):
            user.is_staff = True
            user.is_superuser = True
        if commit:
            user.save()
        return user