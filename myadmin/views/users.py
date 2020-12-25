from os import name
from typing import ContextManager
from django.core import paginator
from django.shortcuts import render
from django.http import HttpResponse, request
from django.db.models import Q
from django.core.paginator import Paginator

from common.models import Users
from datetime import datetime

# 浏览会员
def index(request,pIndex=1):
    # 执行数据查询，并放置到模板中
    umod = Users.objects
    mywhere=[]

    kw = request.GET.get('keyword',None)
    if kw:
        list = umod.filter(Q(username__contains=kw) | Q(name__contains=kw))
        mywhere.append('keyword='+kw)
    else:
        list = umod.filter()

    sex = request.GET.get('sex','')
    if sex !='':
        list = list.filter(sex=sex)
        mywhere.append('sex='+sex)

    pIndex = int(pIndex)
    page = Paginator(list,5)
    maxpages = page.num_pages #最大页数
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #当前页数据
    plist = page.page_range #页码数列表

    context = {'userslist':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,'myadmin/users/index.html',context)


# 会员信息添加表单
def add(request):
    return render(request,'myadmin/users/add.html')

#执行会员信息添加    
def insert(request):
    try:
        ob = Users()
        ob.username = request.POST['username']
        ob.name = request.POST['name']
        #获取密码并md5
        import hashlib
        if request.POST['password'] == request.POST['repassword']:
            m = hashlib.md5() 
            m.update(bytes(request.POST['password'],encoding="utf8"))
            ob.password = m.hexdigest()
            ob.sex = request.POST['sex']
            ob.address = request.POST['address']
            ob.code = request.POST['code']
            ob.phone = request.POST['phone']
            ob.email = request.POST['email']
            ob.state = 1
            ob.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ob.save()
            context = {'info':'添加成功！'}
        else:
            context = {'info' : '2次密码输入不一致！'}
    except Exception as err:
        print(err)
        context = {'info':'添加失败！'}

    return render(request,"myadmin/info.html",context)

# 执行会员信息删除
def delete(request,uid):
    try:
        ob = Users.objects.get(id=uid)
        ob.delete()
        context = {'info':'删除成功！'}
    except:
        context = {'info':'删除失败！'}
    return render(request,"myadmin/info.html",context)

# 打开会员信息编辑表单
def edit(request,uid):
    try:
        ob = Users.objects.get(id=uid)
        context = {'user':ob}
        return render(request,"myadmin/users/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info':'没有找到要修改的信息！'}
    return render(request,"myadmin/info.html",context)

# 执行会员信息编辑
def update(request,uid):
    try:
        ob = Users.objects.get(id=uid)
        ob.name = request.POST['name']
        ob.sex = request.POST['sex']
        ob.address = request.POST['address']
        ob.code = request.POST['code']
        ob.phone = request.POST['phone']
        ob.email = request.POST['email']
        ob.state = request.POST['state']
        ob.save()
        context = {'info':'修改成功！'}
    except Exception as err:
        print(err)
        context = {'info':'修改失败！'}
    return render(request,"myadmin/info.html",context)


# 管理员密码修改
def change(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')
        if new_password != new_password2:
            context = {'info':'2次密码输入不一致'}
        else:
            user = Users.objects.get(name = request.session['adminuser'])
            import hashlib
            m = hashlib.md5() 
            m.update(bytes(request.POST['new_password'],encoding="utf8"))
            user.password = m.hexdigest()
            user.save()
            context = {'info':'密码修改成功'}
        return render(request,"myadmin/info.html",context)
    elif request.method == 'GET':
        return render(request,'myadmin/users/change_password.html')


def resetpass(request,uid):
    '''加载重置会员密码信息页面'''
    try:
        ob = Users.objects.get(id=uid)
        context = {'user':ob}
        return render(request,'myadmin/users/resetpass.html',context)
    except Exception as err:
        print(err)
        context = {'info':'没有找到要修改的信息！'}
        return render(request,'myadmin/info.html',context)


def doresetpass(request,uid):
    '''执行编辑信息'''
    try:
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        if password != repassword:
            context = {'info':'2次密码输入不一致'}
        else:
            ob = Users.objects.get(id=uid)
            import hashlib
            m = hashlib.md5()
            m.update(bytes(request.POST['password'],encoding='utf8'))
            ob.password = m.hexdigest()
            ob.save()
            context = {'info':'密码重置成功'}
    except Exception as err:
        print(err)
        context={'info':'密码重置失败'}
    return render(request,'myadmin/info.html',context)
