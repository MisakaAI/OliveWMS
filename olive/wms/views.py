from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import *
import json

def index(request):
    # return HttpResponse("Hello, world.")
    return render(request, 'wms/index.html')

# 查询
def search(request):
    if request.method == 'GET':
        if request.GET['type'] == 'item':
            if 'v' in request.GET and request.GET['v'] != '':
                r = {i.name:{'unit':i.unit,'price':i.price} for i in item.objects.filter(name__icontains=request.GET['v'])}
            else:
                # r = {i.name:{'unit':i.unit,'price':i.price} for i in item.objects.all()}
                r = {i.name:{'unit':i.unit,'price':i.price} for i in item.objects.order_by("id")[:10]}
        elif request.GET['type'] == 'supplier':
            if 'v' in request.GET and request.GET['v'] != '':
                r = [i.name for i in supplier.objects.filter(name__icontains=request.GET['v'])]
            else:
                r = [i.name for i in supplier.objects.all()]
        elif request.GET['type'] == 'warehouse':
            r = [(i.name,i.id) for i in warehouse.objects.all()]
        elif request.GET['type'] == 'storage_area':
            r = [(i.name,i.id) for i in storage_area.objects.filter(warehouse__id=request.GET['id'])]
        elif request.GET['type'] == 'shelf':
            r = [(i.name,i.id) for i in shelf.objects.filter(storage_area__id=int(request.GET['id']))]
        elif request.GET['type'] == 'storage_location':
            s = shelf.objects.get(id=int(request.GET['id']))
            l = []
            detail = []
            for x in range(s.max_row):
                w = {}
                for y in range(s.max_column):
                    w[str(x+1) + '-' + str(y+1)] = False
                l.append(w)
            sl = storage_location.objects.filter(shelf=s).order_by("row","column")
            if len(sl) != 0:
                for i in sl:
                    l[i.row-1][str(i.row) + '-' + str(i.column)] = True
                    detail.append([str(i.row) + '-' + str(i.column), i.item, i.quantity])
            r=[s.id, s.max_row, s.max_column, l, detail]
        elif request.GET['type'] == 'purchase':
            if 'v' in request.GET and request.GET['v'] != '':
                try:
                    print(request.GET['v'])
                    if len(request.GET['v']) == 8:
                        date = datetime.strptime(request.GET['v'], '%Y%m%d').date()
                        p = Purchase.objects.filter(createtime__date=date).order_by('-createtime')
                        r = {str(i):[i.createtime.date(),i.supplier,i.item_list] for i in p}
                    elif len(request.GET['v']) == 12:
                        date = datetime.strptime(request.GET['v'][:8], '%Y%m%d').date()
                        p = Purchase.objects.filter(createtime__date=date,serial=int(request.GET['v'][-4:])).order_by('-createtime')
                        r = {str(i):[i.createtime.date(),i.supplier,i.item_list] for i in p}
                    else:
                        r = []
                except Exception as e:
                    r = []
            else:
                r = {}
                for i in Purchase.objects.order_by('-createtime')[:10]:
                    r[str(i)] = [i.createtime.date(),i.supplier,i.item_list]

    return JsonResponse(r, safe=False, json_dumps_params={'ensure_ascii': False})

# 提交
def submit(request):
    if request.method == 'POST':
        if request.POST['type'] == "purchase":
            try:
                item_list = json.loads(request.POST['item_list'])
                for i in item_list:
                    i['num'] = int(i['num'])
                    storage = i['storage'].split('-')
                    if len(storage) != 3:
                        raise RuntimeError('储位 {} 不存在'.format(i['storage']))
                    else:
                        for x in storage:
                            try:
                                int(x)
                            except Exception as e:
                                raise RuntimeError('储位 {} 不存在'.format(i['storage']))
                    try:
                        get_shelf = shelf.objects.get(id=int(storage[0]))
                    except Exception as e:
                        raise RuntimeError('储位 {} 不存在'.format(i['storage']))
                    if int(storage[1]) <= 0 or int(storage[1]) > get_shelf.max_row or int(storage[2]) <= 0 or int(storage[2]) > get_shelf.max_column:
                        raise RuntimeError('储位 {} 不存在'.format(i['storage']))
                    v = storage_location.objects.filter(shelf=get_shelf,row=int(storage[1]),column=int(storage[2]),item=i['item'])
                    if len(v) == 0:
                        storage_location.objects.create(shelf=get_shelf,row=int(storage[1]),column=int(storage[2]),item=i['item'],quantity=i['num'])
                    else:
                        v[0].quantity += int(i['num'])
                        v[0].save()
                p = Purchase.objects.filter(createtime__date=datetime.now().date())
                if len(p) == 0:
                    Purchase.objects.create(serial=1,supplier=request.POST['supplier'],item_list=item_list)
                else:
                    Purchase.objects.create(serial=p.order_by("createtime").last().serial+1,supplier=request.POST['supplier'],item_list=item_list)
                r = { "status":"success" }
            except Exception as e:
                r = { "status":"error" ,"info": str(e)}
        return JsonResponse(r, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        return HttpResponse('error. It is not POST')

# 库存统计
def count(request):
    return render(request, 'wms/count.html')
# 生产入库
def put_in(request):
    return render(request, 'wms/put_in.html')
# 系统设置
def setting(request):
    return render(request, 'wms/setting.html')
# 进货
def purchase(request):
    return render(request, 'wms/purchase.html')
# 退货
def purchase_return(request):
    return render(request, 'wms/purchase_return.html')
# 领料
def get_material(request):
    return render(request, 'wms/get_material.html')
# 退料
def material_return(request):
    return render(request, 'wms/material_return.html')
# 销售
def sale(request):
    return render(request, 'wms/sale.html')
# 销退
def sale_return(request):
    return render(request, 'wms/sale_return.html')
# 盘点
def check(request):
    return render(request, 'wms/check.html')