
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    # =====================================================
    # الصفحة الرئيسية
    # =====================================================

    path(
        '',
        views.coffee_list,
        name='coffee_list'
    ),


    # =====================================================
    # التسجيل وتسجيل الدخول
    # =====================================================

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='coffee/login.html',
            redirect_authenticated_user=True
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='coffee_list'
        ),
        name='logout'
    ),


    # =====================================================
    # لوحة التحكم
    # =====================================================

    path(
        'dashboard/',
        views.dashboard_view,
        name='dashboard'
    ),


    # =====================================================
    # البريد الإلكتروني الحقيقي
    # =====================================================

    path(
        'send-email/',
        views.send_email_view,
        name='send_email'
    ),


    # =====================================================
    # سلة التسوق
    # =====================================================

    path(
        'cart/add/<int:item_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/',
        views.view_cart,
        name='view_cart'
    ),

    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),


    # =====================================================
    # مسارات النماذج
    # =====================================================

    path(
        'add-user/',
        views.add_user_view,
        name='add_user'
    ),

    path(
        'add-coffee/',
        views.add_coffee_view,
        name='add_coffee'
    ),


    # =====================================================
    # QuerySet Demo
    # =====================================================

    path(
        'queryset-demo/',
        views.queryset_demo_view,
        name='queryset_demo'
    ),

    path(
        'all-forms/',
        views.all_forms_view,
        name='all_forms'
    ),
]

