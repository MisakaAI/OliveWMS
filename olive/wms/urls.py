from django.urls import path
from . import views

urlpatterns = [
    # 首页
    path("", views.index, name="index"),
    # 库存查询
    path("search", views.search, name="search"),
    # 提交接口
    path("submit", views.submit, name="submit"),
    # 库存统计
    path("count", views.count, name="count"),
    # 生产入库
    path("put_in", views.put_in, name="put_in"),
    # 系统设置
    path("setting", views.setting, name="setting"),
    # 进货
    path("purchase", views.purchase, name="purchase"),
    # 退货
    path("purchase_return", views.purchase_return, name="purchase_return"),
    # 领料
    path("get_material", views.get_material, name="get_material"),
    # 退料
    path("material_return", views.material_return, name="material_return"),
    # 销售
    path("sale", views.sale, name="sale"),
    # 销退
    path("sale_return", views.sale_return, name="sale_return"),
    # 盘点
    path("check", views.check, name="check"),
]