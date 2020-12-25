"""myobject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.urls import path
from myadmin.views import index,users,type,goods,orders

app_name = 'myadmin' 

urlpatterns = [
    path('',index.index,name='myadmin_index'),
    path('users/(?P<pIndex>[0-9]+)',users.index,name="myadmin_users_index"),
    path('users/add/',users.add,name="myadmin_users_add"),
    path('users/insert/',users.insert,name="myadmin_users_insert"),
    path('users/del/(?P<uid>[0-9]+)',users.delete,name="myadmin_users_del"),
    path('users/edit/(?P<uid>[0-9]+)',users.edit,name="myadmin_users_edit"),
    path('users/update/(?P<uid>[0-9]+)',users.update,name="myadmin_users_update"),
    path('users/resetpass/(?P<uid>[0-9]+)',users.resetpass,name='myadmin_users_resetpass'),
    path('users/doresetpass/(?P<uid>[0-9]+)',users.doresetpass,name='myadmin_users_doresetpass'),
    path('user/change/',users.change,name="myadmin_users_change"),
    path('login',index.login,name="myadmin_login"),
    path('logout/',index.lgout,name="myadmin_logout"),
    path('verify',index.verify,name='myadmin_verify'),#验证码
    # 后台商品类别信息管理
    path('type/', type.index, name="myadmin_type_index"),
    path('type/add/(?P<tid>[0-9]+)', type.add, name="myadmin_type_add"),
    path('type/insert$', type.insert, name="myadmin_type_insert"),
    path('type/del/(?P<tid>[0-9]+)', type.delete, name="myadmin_type_del"),
    path('type/edit/(?P<tid>[0-9]+)', type.edit, name="myadmin_type_edit"),
    path('type/update/(?P<tid>[0-9]+)', type.update, name="myadmin_type_update"),
    # 后台商品信息管理
    path('goods/(?P<pIndex>[0-9]+)', goods.index, name="myadmin_goods_index"),
    path('goods/add', goods.add, name="myadmin_goods_add"),
    path('goods/insert', goods.insert, name="myadmin_goods_insert"),
    path('goods/del/(?P<gid>[0-9]+)', goods.delete, name="myadmin_goods_del"),
    path('goods/edit/(?P<gid>[0-9]+)', goods.edit, name="myadmin_goods_edit"),
    path('goods/update/(?P<gid>[0-9]+)', goods.update, name="myadmin_goods_update"),
     # 订单信息管理路由
    path('orders', orders.index, name="myadmin_orders_index"),
    path('orders/(?P<pIndex>[0-9]+)', orders.index, name="myadmin_orders_index"),
    path('orders/detail/(?P<oid>[0-9]+)', orders.detail, name="myadmin_orders_detail"),
    path('orders/state',orders.state, name="myadmin_orders_state"),
]
