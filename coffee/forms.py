from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import CoffeeItem

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
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('is_staff_user'):
            user.is_staff = True
            user.is_superuser = True
        if commit:
            user.save()
        return user

# أضف هذا الفورم هنا لكي يتم استيراده بنجاح في ملف views.py
class CoffeeItemForm(forms.ModelForm):
    class Meta:
        model = CoffeeItem
        fields = ['name', 'price', 'roast_level', 'branch_name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم القهوة'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'السعر'}),
            'roast_level': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'درجة التحميص'}),
            'branch_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم الفرع'}),
        }