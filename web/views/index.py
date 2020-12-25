import random
from django.core.checks.messages import Info
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.core.mail import send_mail

from common.models import Goods, Types, Users
from django.core.paginator import Paginator

import json
from datetime import datetime

# Create your views here.
# 加载公共信息
def loadinfo(request):
    context = {}
    lists = Types.objects.filter(pid=0)
    for cc in lists:
        cc.goo = Goods.objects.filter(typeid__in=Types.objects.only('id').filter(pid=cc.id))
        # 添加子类名属性
        cc.cca = Types.objects.filter(pid=cc.id)
        for ff in cc.cca:
            # 添加子类名所属商品
            ff.good = Goods.objects.filter(typeid=ff.id)[:4]
    context['typelist'] = lists  
    list1 = Goods.objects.all().order_by('-id')[:4]
    goodshot1 = Goods.objects.all().order_by('-clicknum')[:5]
    goodshot2 = Goods.objects.all().order_by('-clicknum')[5:10]
    context['list1'] = list1
    context['goodshot1'] = goodshot1
    context['goodshot2'] = goodshot2
    return context


def index(request):
    '''项目前台首页'''
    context = loadinfo(request)
    return render(request,"web/index.html",context)


# 价格排序
def lists1(request,pIndex=1):
    context = loadinfo(request)
    # 获取商品信息查询对象
    mod = Goods.objects
    mywhere = []
    # 判断添加搜索条件
    tid = int(request.GET.get('tid',0))
    print(tid)
    if tid > 0:
        ll = Types.objects.only('id').filter(pid=tid)
        list = mod.filter(typeid__in=Types.objects.only('id').filter(pid=tid)).order_by('-price')
        if list.count() < 1:
            list = mod.filter(typeid=tid).order_by('-price')
        mywhere.append('tid='+str(tid))
    else:
        list = mod.filter().order_by('-price')
        ll =[]
    kw = request.GET.get('keyword',None)
    if kw:
        # 查询商品名中只要含有关键字的都可以,精确大小写
        list = list.filter(goods__contains=kw)
        mywhere.append("keyword="+kw)
    pIndex = int(pIndex)
    page = Paginator(list,8) #以5条每页创建分页对象
    maxpages = page.num_pages #最大页数
    #判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #当前页数据
    plist = page.page_range   #页码数列表

    #封装信息加载模板输出
    context['ll'] = ll
    context['goodslist'] = list2
    context['plist'] = plist
    context['pIndex'] = pIndex
    context['maxpages'] = maxpages
    context['mywhere'] = mywhere
    context['tid'] = int(tid)
    return render(request,"web/list1.html",context)



def lists(request,pIndex=1):
    '''商品列表页'''
    context = loadinfo(request)
    # 获取商品信息查询对象
    mod = Goods.objects
    mywhere = []
    # 判断添加搜索条件
    tid = int(request.GET.get('tid',0))
    print(tid)
    if tid > 0:
        ll = Types.objects.only('id').filter(pid=tid)
        list = mod.filter(typeid__in=Types.objects.only('id').filter(pid=tid))
        if list.count() < 1:
            list = mod.filter(typeid=tid)
        mywhere.append('tid='+str(tid))
    else:
        list = mod.filter()
        ll =[]
    
    # 获取，判断并封装keyword键搜索
    kw = request.GET.get('keyword',None)
    if kw:
        # 查询商品名中只要含有关键字的都可以,精确大小写
        list = list.filter(goods__contains=kw)
        mywhere.append("keyword="+kw)

    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list,8) #以5条每页创建分页对象
    maxpages = page.num_pages #最大页数
    #判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #当前页数据
    plist = page.page_range   #页码数列表

    #封装信息加载模板输出
    context['ll'] = ll
    context['goodslist'] = list2
    context['plist'] = plist
    context['pIndex'] = pIndex
    context['maxpages'] = maxpages
    context['mywhere'] = mywhere
    context['tid'] = int(tid)
    return render(request,"web/list.html",context)


def detail(request,gid):
    '''商品详情页'''
    context = loadinfo(request)
    #加载商品详情信息
    ob = Goods.objects.get(id=gid)
    ob.clicknum += 1 # 点击量加1
    ob.save()
    context['goods'] = ob
    return render(request,"web/detail.html",context)

def login(requset):
    return render(requset,'web/login.html')

def dologin(request):
    '''会员执行登录'''
    # 校验验证码
    verifycode = request.session['verifycode']
    code = request.POST['code']
    if verifycode != code:
        context = {'info':'验证码错误！'}
        return render(request,"web/login.html",context)
    
    try:
        #根据账号获取登录者信息
        user = Users.objects.get(username=request.POST['username'])
        #判断当前用户是否是后台管理员用户
        if user.state == 0 or user.state == 1:
            # 验证密码
            import hashlib
            m = hashlib.md5() 
            m.update(bytes(request.POST['password'],encoding="utf8"))
            if user.password == m.hexdigest():
                # 此处登录成功，将当前登录信息放入到session中，并跳转页面
                data = json.dumps(user.toDict(), default=str, ensure_ascii=False)
                data = json.loads(data)
                request.session['vipuser'] = data

                return redirect(reverse('web:index'))
            else:
                context = {'info':'登录密码错误！'}
        else:
            context = {'info':'此用户为非法用户！'}
    except:
            context = {'info':'登录账号错误！'}
    return render(request,"web/login.html",context)

def logout(request):
    '''会员退出'''
    # 清除登录的session信息
    del request.session['vipuser']
    # 跳转登录页面（url地址改变）
    return redirect(reverse('web:login'))

#注册页面
def register(request):
    return render(request,'web/register.html')

def regupdate(request):
    #判断两次密码是否一致
    pwd = request.POST['passwd']
    repwd = request.POST['repasswd']
    name = request.POST['username']
    if Users.objects.filter(username=name):
        content = {'info':'用户名已被注册'}
    else:
        if repwd != pwd:
            content = {"info":"两次密码不相同,请重新输入!"}
            return render(request,"web/register.html",content)
        try:
            gb = Users()
            gb.username = request.POST['username']
            import hashlib
            m = hashlib.md5()
            m.update(bytes(request.POST['passwd'],encoding="utf8"))
            gb.password = m.hexdigest()
            gb.email = request.POST['email']
            gb.phone = request.POST['phone']
            gb.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            gb.state = 1
            gb.save()
            content={"info":"注册成功!可以登录了"}
            return render(request,"web/register.html",content)
        except:
            content={"info":"注册失败!"}
    return render(request,"web/register.html",content)

# 忘记密码
def forget(request):
    return render(request,'web/forget.html')

def reforget(request):
    email = request.POST['email']
    name = request.POST['username']
    try:
        user = Users.objects.filter(username=name).first()
        if user.email != email:
            content = {'info':'用户名或邮箱错误'}
            return render(request,'web/forget.html',content)
        else:
            # 生成6为随机数验证码
            email_code = '%06d' % random.randint(0,999999)
            send_mail(
                '欢乐购商城忘记密码邮箱验证',
                '验证码为:' + email_code,
                'cfxcheer@qq.com',
                [ email ]
            )
            request.session['email_code1'] = email_code
            request.session['name1'] = name
            content = {'info':'注意查看邮箱验证码信息！'}
            return render(request,'web/newforget.html',content)
    except:
        content ={'info':'预期之外的错误'}
        return render(request,'web/forget.html',content)


def newforget(requset):
    email_code = requset.POST['code']
    pwd = requset.POST['password']
    repwd = requset.POST['repassword']
    if email_code == requset.session['email_code1'] and pwd == repwd:
        name = requset.session['name1']
        user = Users.objects.filter(username=name).first()
        import hashlib
        m = hashlib.md5()
        m.update(bytes(pwd,encoding='utf8'))
        user.password = m.hexdigest()
        user.save()
        context = {'info':'修改成功，请登录！'}
        return render(requset,'web/login.html',context)
    else:
        context = {'info':'验证码或密码输入错误'}
        return render(requset,'web/newforget.html',context)

def cartadd(request,gid):
    return render(request,'web/login.html')
