from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, F
from .forms import CustomUserCreationForm, AdminUserCreationForm, CoffeeItemForm
from .models import CoffeeItem, Order, OrderItem

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'coffee/register.html', {'form': form})

@login_required
def dashboard_view(request):
    return render(request, 'coffee/dashboard.html')

@staff_member_required
def add_user_view(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AdminUserCreationForm()
    return render(request, 'coffee/add_user.html', {'form': form})

# دالة إضافة صنف قهوة جديد باستخدام النموذج (Form)
@staff_member_required
def add_coffee_view(request):
    if request.method == 'POST':
        form = CoffeeItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coffee_list')
    else:
        form = CoffeeItemForm()
    return render(request, 'coffee/form_template.html', {'form': form, 'title': 'إضافة صنف قهوة جديد'})

# دالة مخصصة لجمع وعرض النماذج الثلاثة معاً في صفحة واحدة
def all_forms_view(request):
    form1 = CustomUserCreationForm(prefix='form1')
    form2 = AdminUserCreationForm(prefix='form2')
    form3 = CoffeeItemForm(prefix='form3')

    if request.method == 'POST':
        form1 = CustomUserCreationForm(request.POST, prefix='form1')
        form2 = AdminUserCreationForm(request.POST, prefix='form2')
        form3 = CoffeeItemForm(request.POST, prefix='form3')

        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            form1.save()
            form2.save()
            form3.save()
            return redirect('coffee_list')

    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3,
    }
    return render(request, 'coffee/all_forms.html', context)

def coffee_list(request):
    query = request.GET.get('q', '')
    if query:
        coffees = CoffeeItem.objects.filter(name__icontains=query) | CoffeeItem.objects.filter(branch_name__icontains=query)
    else:
        coffees = CoffeeItem.objects.all()
    return render(request, 'coffee/coffee_list.html', {'coffees': coffees, 'query': query})

def add_to_cart(request, item_id):
    if not request.user.is_authenticated:
        return redirect('login')
    coffee = get_object_or_404(CoffeeItem, id=item_id)
    
    order = Order.objects.filter(user=request.user, is_completed=False).first()
    if not order:
        order = Order.objects.create(user=request.user, is_completed=False)
        
    order_item, created = OrderItem.objects.get_or_create(order=order, coffee=coffee)
    if not created:
        order_item.quantity += 1
        order_item.save()
    return redirect('view_cart')

def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    order = Order.objects.filter(user=request.user, is_completed=False).first()
    return render(request, 'coffee/cart.html', {'order': order})

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    order = Order.objects.filter(user=request.user, is_completed=False).first()
    if order:
        order.is_completed = True
        order.save()
    return redirect('coffee_list')

# دالة مخصصة تجمع 10 دوال QuerySet لتلبية متطلبات التكليف
def queryset_demo_view(request):
    # 1. all(): جلب كافة العناصر
    all_coffees = CoffeeItem.objects.all()

    # 2. filter(): تصفية العناصر بشرط معين
    dark_coffees = CoffeeItem.objects.filter(roast_level__icontains='Dark')

    # 3. exclude(): استبعاد عناصر بشرط معين
    affordable_coffees = CoffeeItem.objects.exclude(price__gt=5000.00)

    # 4. get(): جلب عنصر واحد محدد بدقة
    single_coffee = CoffeeItem.objects.filter(id=1).first()

    # 5. order_by(): ترتيب العناصر تنازلياً حسب السعر
    sorted_coffees = CoffeeItem.objects.order_by('-price')

    # 6. count(): حساب عدد الطلبات المكتملة
    completed_orders_count = Order.objects.filter(is_completed=True).count()

    # 7. exists(): التحقق من وجود نتائج تطابق الاستعلام (True / False)
    has_items = CoffeeItem.objects.filter(price__lte=5000).exists()

    # 8. values(): جلب الحقول المحددة فقط كقواميس
    coffee_data = CoffeeItem.objects.values('name', 'price')

    # 9. distinct(): منع تكرار النتائج بناءً على الفرع
    unique_branches = CoffeeItem.objects.values('branch_name').distinct()

    # 10. aggregate(): إجراء عملية حسابية تجميعية (مجموع مبيعات الطلبات المكتملة)
    total_sales_result = OrderItem.objects.filter(order__is_completed=True).aggregate(
        total=Sum(F('quantity') * F('coffee__price'))
    )
    total_sales = total_sales_result['total'] if total_sales_result['total'] is not None else 0.00

    context = {
        'all_coffees': all_coffees,
        'dark_coffees': dark_coffees,
        'affordable_coffees': affordable_coffees,
        'single_coffee': single_coffee,
        'sorted_coffees': sorted_coffees,
        'completed_orders_count': completed_orders_count,
        'has_items': has_items,
        'coffee_data': coffee_data,
        'unique_branches': unique_branches,
        'total_sales': total_sales,
    }
    return render(request, 'coffee/queryset_demo.html', context)