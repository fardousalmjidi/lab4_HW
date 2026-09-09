from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, F
from django.core.mail import send_mail

from .forms import (
    CustomUserCreationForm,
    AdminUserCreationForm,
    CoffeeItemForm,
    EmailMessageForm
)

from .models import CoffeeItem, Order, OrderItem


# ==========================================
# 1. قسم دوال النماذج وتوثيق الحماية
# ==========================================

def register_view(request):
    """
    إذا كان المستخدم مسجلاً دخوله مسبقاً، يتم منعه من الوصول إلى صفحة التسجيل
    ويتم إعادة توجيهه تلقائياً إلى الصفحة الرئيسية (coffee_list).
    """

    if request.user.is_authenticated:
        return redirect('coffee_list')

    if request.method == 'POST':

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('dashboard')

    else:

        form = CustomUserCreationForm()

    return render(
        request,
        'coffee/register.html',
        {
            'form': form
        }
    )


@login_required
def dashboard_view(request):
    """عرض لوحة التحكم الخاصة بالمستخدمين المسجلين."""

    return render(
        request,
        'coffee/dashboard.html'
    )


@staff_member_required
def add_user_view(request):
    """نموذج خاص بالمشرفين (Staff) لإنشاء مستخدمين جدد أو أدمن."""

    if request.method == 'POST':

        form = AdminUserCreationForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('dashboard')

    else:

        form = AdminUserCreationForm()

    return render(
        request,
        'coffee/add_user.html',
        {
            'form': form
        }
    )


@staff_member_required
def add_coffee_view(request):
    """نموذج لإضافة صنف قهوة جديد إلى قاعدة البيانات."""

    if request.method == 'POST':

        form = CoffeeItemForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('coffee_list')

    else:

        form = CoffeeItemForm()

    return render(
        request,
        'coffee/form_template.html',
        {
            'form': form,
            'title': 'إضافة صنف قهوة جديد'
        }
    )


def all_forms_view(request):
    """
    دالة مخصصة لجمع وعرض النماذج الثلاثة معاً في صفحة واحدة
    باستخدام الـ Prefixes لتجنب تداخل بيانات الحفظ.
    """

    form1 = CustomUserCreationForm(prefix='form1')

    form2 = AdminUserCreationForm(prefix='form2')

    form3 = CoffeeItemForm(prefix='form3')

    if request.method == 'POST':

        form1 = CustomUserCreationForm(
            request.POST,
            prefix='form1'
        )

        form2 = AdminUserCreationForm(
            request.POST,
            prefix='form2'
        )

        form3 = CoffeeItemForm(
            request.POST,
            prefix='form3'
        )

        if (
            form1.is_valid()
            and form2.is_valid()
            and form3.is_valid()
        ):

            form1.save()

            form2.save()

            form3.save()

            return redirect('coffee_list')

    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3,
    }

    return render(
        request,
        'coffee/all_forms.html',
        context
    )


# ==========================================
# 2. إرسال بريد إلكتروني حقيقي
# ==========================================

@login_required
def send_email_view(request):
    """
    صفحة إرسال بريد إلكتروني حقيقي باستخدام Gmail SMTP.
    """

    if request.method == 'POST':

        form = EmailMessageForm(request.POST)

        if form.is_valid():

            recipient = form.cleaned_data['recipient']

            subject = form.cleaned_data['subject']

            message = form.cleaned_data['message']

            try:

                send_mail(
                    subject=subject,
                    message=message,
                    from_email=None,
                    recipient_list=[recipient],
                    fail_silently=False,
                )

                return render(
                    request,
                    'coffee/send_email.html',
                    {
                        'form': EmailMessageForm(),
                        'success': True
                    }
                )

            except Exception as e:

                return render(
                    request,
                    'coffee/send_email.html',
                    {
                        'form': form,
                        'error': str(e)
                    }
                )

    else:

        form = EmailMessageForm()

    return render(
        request,
        'coffee/send_email.html',
        {
            'form': form
        }
    )


# ==========================================
# 3. قسم المتجر والعمليات الأساسية
# ==========================================

def coffee_list(request):
    """عرض قائمة الأصناف مع إمكانية البحث والفلترة بالاسم أو الفرع."""

    query = request.GET.get('q', '')

    if query:

        coffees = (
            CoffeeItem.objects.filter(
                name__icontains=query
            )
            |
            CoffeeItem.objects.filter(
                branch_name__icontains=query
            )
        )

    else:

        coffees = CoffeeItem.objects.all()

    return render(
        request,
        'coffee/coffee_list.html',
        {
            'coffees': coffees,
            'query': query
        }
    )


def add_to_cart(request, item_id):
    """إضافة صنف معين إلى سلة تسوق المستخدم الحالي."""

    if not request.user.is_authenticated:
        return redirect('login')

    coffee = get_object_or_404(
        CoffeeItem,
        id=item_id
    )

    order = Order.objects.filter(
        user=request.user,
        is_completed=False
    ).first()

    if not order:

        order = Order.objects.create(
            user=request.user,
            is_completed=False
        )

    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        coffee=coffee
    )

    if not created:

        order_item.quantity += 1

        order_item.save()

    return redirect('view_cart')


def view_cart(request):
    """عرض محتويات سلة التسوق الخاصة بالمستخدم."""

    if not request.user.is_authenticated:
        return redirect('login')

    order = Order.objects.filter(
        user=request.user,
        is_completed=False
    ).first()

    return render(
        request,
        'coffee/cart.html',
        {
            'order': order
        }
    )


def checkout(request):
    """إتمام الطلب وتحويل حالة السلة إلى مكتملة وإرسال بريد تأكيد حقيقي."""

    if not request.user.is_authenticated:
        return redirect('login')

    order = Order.objects.filter(
        user=request.user,
        is_completed=False
    ).first()

    if order:

        order.is_completed = True

        order.save()

        subject = 'تأكيد طلبك من متجر القهوة'

        message = (
            f'مرحباً {request.user.username}،\n\n'
            f'تم استلام طلبك بنجاح وسنقوم بتجهيزه في أقرب وقت.\n'
            f'شكراً لتسوقك معنا!'
        )

        recipient_list = (
            [request.user.email]
            if request.user.email
            else []
        )

        if recipient_list:

            try:

                send_mail(
                    subject,
                    message,
                    None,
                    recipient_list,
                    fail_silently=False,
                )

            except Exception as e:

                pass

    return redirect('coffee_list')


# ==========================================
# 4. قسم استعلامات قاعدة البيانات
# ==========================================

def queryset_demo_view(request):
    """
    دالة مخصصة تجمع 10 دوال مختلفة لـ QuerySet لتلبية متطلبات التكليف،
    وتقوم بعرض النتائج وتوثيق كل دالة بتعليق توضيحي خاص بها.
    """

    # 1. all():
    # استرجاع كافة السجلات والأصناف من الجدول

    all_coffees = CoffeeItem.objects.all()


    # 2. filter():
    # تصفية السجلات بناءً على شرط مطابقة
    # أصناف التحميص الغامق

    dark_coffees = CoffeeItem.objects.filter(
        roast_level__icontains='Dark'
    )


    # 3. exclude():
    # استبعاد السجلات التي تحقق شرطاً معيناً

    affordable_coffees = CoffeeItem.objects.exclude(
        price__gt=5000.00
    )


    # 4. filter().first():
    # جلب سجل واحد محدد بناءً على المعرف

    single_coffee = CoffeeItem.objects.filter(
        id=1
    ).first()


    # 5. order_by():
    # ترتيب السجلات حسب السعر تنازلياً

    sorted_coffees = CoffeeItem.objects.order_by(
        '-price'
    )


    # 6. count():
    # حساب عدد الطلبات المكتملة

    completed_orders_count = Order.objects.filter(
        is_completed=True
    ).count()


    # 7. exists():
    # التحقق من وجود بيانات مطابقة للاستعلام

    has_items = CoffeeItem.objects.filter(
        price__lte=5000
    ).exists()


    # 8. values():
    # استرجاع حقول محددة فقط

    coffee_data = CoffeeItem.objects.values(
        'name',
        'price'
    )


    # 9. values().distinct():
    # استرجاع الفروع المختلفة بدون تكرار

    unique_branches = CoffeeItem.objects.values(
        'branch_name'
    ).distinct()


    # 10. aggregate():
    # حساب إجمالي المبيعات

    total_sales_result = OrderItem.objects.filter(
        order__is_completed=True
    ).aggregate(
        total=Sum(
            F('quantity') *
            F('coffee__price')
        )
    )

    total_sales = (
        total_sales_result['total']
        if total_sales_result['total'] is not None
        else 0.00
    )


    context = {
        'all_coffees': all_coffees,

        'dark_coffees': dark_coffees,

        'affordable_coffees': affordable_coffees,

        'single_coffee': single_coffee,

        'sorted_coffees': sorted_coffees,

        'completed_orders_count':
            completed_orders_count,

        'has_items':
            has_items,

        'coffee_data':
            coffee_data,

        'unique_branches':
            unique_branches,

        'total_sales':
            total_sales,
    }

    return render(
        request,
        'coffee/queryset_demo.html',
        context
    )