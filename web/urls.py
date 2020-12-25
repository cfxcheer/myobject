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
from web import views
from web.views.index import index, lists1
from django.contrib import admin
from django.urls import path
from web.views import index,cart,orders,vip

app_name = 'web' 

urlpatterns = [
    #path('admin/', admin.site.urls),
    #网站前台
    path('',index.index,name="index"), #首页
    path('list',index.lists,name="list"), #商品列表展示
    path('list/(?P<pIndex>[0-9]+)',index.lists,name="list"), #分页商品列表展示
    path('list1/',index.lists1,name='list1'),#价格排序
    path('list1/(?P<pIndex>[0-9]+)',index.lists1,name="list1"),
    path('detail/(?P<gid>[0-9]+)',index.detail,name="detail"), #商品详情

    # 会员及个人中心等路由配置
    path('login', index.login, name="login"),
    path('dologin', index.dologin, name="dologin"),
    path('logout', index.logout, name="logout"),
    # 注册页面
    path('register',index.register,name='register'),
    path('regupdate',index.regupdate,name='regupdate'),
    # 修改密码
    path('forget',index.forget,name='forget'),
    path('reforget',index.reforget,name='reforget'),
    path('newforget',index.newforget,name='newforget'),
    path('cartadd/(?P<gid>[0-9]+)',index.cartadd,name='cartadd'),
    # 购物车路由
    path('cart$', cart.index,name='cart_index'), #浏览购物车
    path('cart/add/(?P<gid>[0-9]+)', cart.add,name='cart_add'), #添加购物车
    path('cart/del/(?P<gid>[0-9]+)', cart.delete,name='cart_del'), #从购物车中删除一个商品
    path('cart/clear', cart.clear,name='cart_clear'), #清空购物车
    path('cart/change', cart.change,name='cart_change'), #更改购物车中商品数量
    # 订单处理
    path('orders/add', orders.add,name='orders_add'), #订单的表单页
    path('orders/confirm$', orders.confirm,name='orders_confirm'), #订单确认页
    path('orders/insert$', orders.insert,name='orders_insert'), #执行订单添加操作
     # 会员中心
    path('vip/orders', vip.viporders,name='vip_orders'), #会员中心我的订单
    path('vip/odstate', vip.odstate,name='vip_odstate'), #修改订单状态（确认收货）
    path('vip/viporders1',vip.viporders1,name='vip_orders1'),
    #url(r'^vip/info$', vip.info,name='vip_info'), #会员中心的个人信息
    #url(r'^vip/update$', vip.update,name='vip_update'), #执行修改会员信息
    #url(r'^vip/resetps$', vip.resetps,name='vip_resetps'), #重置密码表单
    #url(r'^vip/doresetps$', vip.doresetps,name='vip_doresetps'), #执行重置密码
]
