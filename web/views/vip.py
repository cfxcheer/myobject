from django.shortcuts import render,reverse,redirect
from django.http import HttpResponse

from common.models import Users,Goods,Types,Orders,Detail

# 公共信息加载
def loadinfo(request):
    '''公共信息加载'''
    context = {}
    lists = Types.objects.filter(pid=0)
    context['typelist'] = lists
    return context

# 我的订单
def viporders(request):
    '''当前用户订单'''
    context = loadinfo(request)
    # 获取当前用户的所有订单信息
    odlist = Orders.objects.filter(uid=request.session['vipuser']['id']).order_by('-addtime')
    # 遍历当前用户的所有订单，添加他的订单详情
    for od in odlist:
        delist = Detail.objects.filter(orderid=od.id)
        # 遍历每个商品详情，从Goods中获取对应的图片
        for og in delist:
            og.picname = Goods.objects.only('picname').get(id=og.goodsid).picname
        od.detaillist = delist
    # 将整理好的订单信息放置到模板遍历中
    context['orderslist'] = odlist
    return render(request,"web/viporders.html",context)


def viporders1(request):
    context = loadinfo(request)
    mywhere=[]
    # 获取当前用户的所有订单信息
    odlist = Orders.objects.filter(uid=request.session['vipuser']['id']).order_by('-addtime')
    # 遍历当前用户的所有订单，添加他的订单详情

    for od in odlist:
        delist = Detail.objects.filter(orderid=od.id)
        # 遍历每个商品详情，从Goods中获取对应的图片
        for ob in delist:
            ll = Detail.objects.filter(goodsid=ob.goodsid)
            if len(ll)>1:
                mywhere.append(od)

    for od in mywhere:
        delist =  Detail.objects.filter(orderid=od.id)
        for og in delist:
            og.picname = Goods.objects.only('picname').get(id=og.goodsid).picname
        od.detaillist = delist
    # 将整理好的订单信息放置到模板遍历中
    context['orderslist'] = mywhere
    return render(request,"web/viporders1.html",context)


def odstate(request):
    ''' 修改订单状态 '''
    try:
        oid = request.GET.get("oid",'0')
        ob = Orders.objects.get(id=oid)
        ob.state = request.GET['state']
        ob.save()
        return redirect(reverse('web:vip_orders'))
    except Exception as err:
        print(err)
        return HttpResponse("订单处理失败！")