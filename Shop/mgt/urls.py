from django.contrib import admin
from django.urls import path, re_path
from .views import *
# Create your views here.


urlpatterns = [
    # 商品
    path('shop/',shop_list_view,name="shop_list"),
    path('shop/<int:category_id>/',shop_list_view,name="shop_list_type"),
    path('shop/add/',shop_add_view,name="shop_add"),
    path('shop/edit/<int:id>/',shop_edit_view,name="shop_edit"),
    path('shop/del/<int:id>/',shop_del_view,name="shop_del"),

    # 分類
    path('category/',category_list_view,name="category_list"),
    path('category/addedit/', category_addedit_view, name="category_add"),
    path('category/addedit/<int:id>/',category_addedit_view,name="category_edit"),

    # 使用者管理
    path('user/', user_list_view, name="user_list"),
    path('user/add/', user_add_view, name="user_add"),
    path('user/add/<int:id>/',user_add_view,name="user_edit"),
    path('user/del/<int:id>/',user_del_view,name="user_del"),


    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),


    path('valid_img/', GetValidImg.as_view(),name="valid_img"),




    #path('category/',category_list_view,name="category_list"),
]
