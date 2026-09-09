from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import CoffeeItem


# =========================================================
# نموذج إنشاء مستخدم عادي
# =========================================================

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email']


# =========================================================
# نموذج إنشاء مستخدم بواسطة الأدمن
# =========================================================

class AdminUserCreationForm(UserCreationForm):

    is_staff_user = forms.BooleanField(
        required=False,
        label="منحه صلاحيات الأدمن (Admin)",
        widget=forms.CheckboxInput(
            attrs={
                'style': 'margin-right: 10px;'
            }
        )
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


# =========================================================
# نموذج إضافة صنف قهوة
# =========================================================

class CoffeeItemForm(forms.ModelForm):

    class Meta:

        model = CoffeeItem

        fields = [
            'name',
            'price',
            'roast_level',
            'branch_name'
        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'اسم القهوة'
                }
            ),

            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'السعر'
                }
            ),

            'roast_level': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'درجة التحميص'
                }
            ),

            'branch_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'اسم الفرع'
                }
            ),
        }


# =========================================================
# نموذج إرسال البريد الإلكتروني
# =========================================================

class EmailMessageForm(forms.Form):

    recipient = forms.EmailField(
        label="البريد الإلكتروني للمستلم",

        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'example@gmail.com',
                'dir': 'ltr'
            }
        )
    )

    subject = forms.CharField(
        label="عنوان الرسالة",

        max_length=200,

        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'عنوان الرسالة'
            }
        )
    )

    message = forms.CharField(
        label="محتوى الرسالة",

        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'اكتب محتوى الرسالة هنا...',
                'rows': 8
            }
        )
    )