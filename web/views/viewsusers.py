from django.shortcuts import render,redirect,reverse

from common.models import Types,Goods,Users,Orders,Detail

#反向需要模块
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import redirect

#分页需要模块
from django.core.paginator import Paginator
#导入模版
import os,time,json

#==========个人中心=======================
def member(request):
    print(request.session['vipuser']['id'])
    try:
        ob = Orders.objects.filter(uid = request.session['vipuser']['id'])
        #代发货订单数量
        newon = 0
        #已发货订单数量
        faon = 0
        for orders in ob:
            #代发货订单
            if orders.state == 0:
                newon += 1
            #已发货订单数量
            elif orders.state == 1:
            	faon += 1
        content = {'newon':newon,'faon':faon}
        return render(request,'web/member.html',content)
    except os.error:
        print(OSError)
        content = {'info':'当前用户未登录,请登录'}
        return render(request,'web/login.html',content)

def memberdetail(request):
    try:
        ub = Users.objects.get(id = request.session['vipuser']['id'])
        content = {'userlist':ub}
        return render(request,'web/memberdetail.html',content)
    except :
        content = {'info':'当前用户未登录,请登录'}
        return render(request,'web/login.html',content)

def memberchange(request):
    #判断两次输入密码是否一直
    pwd = request.POST['passwd']
    repwd = request.POST['repasswd']
    if  repwd != pwd:
        ub = Users.objects.get(id = request.session['vipuser']['id'])
        content={"info":"两次密码不相同,请重新输入!",'userlist':ub}
        return render(request,"web/memberdetail.html",content)
    ub = Users.objects.get(id = request.session['vipuser']['id'])
    if pwd != '':
    #获取密码并md5
        import hashlib
        m = hashlib.md5() 
        m.update(bytes(request.POST['passwd'],encoding="utf8"))
        ub.password = m.hexdigest()
    
    ub.name = request.POST['name']
    ub.email = request.POST['email']
    ub.phone = request.POST['phone']
    ub.save()
    content={'info':'修改成功'}
    return redirect(reverse('web:memberdetail'),content)
#==========个人中心=======================