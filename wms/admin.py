from django.contrib import admin
from .models import *

# 供应商
admin.site.register(Supplier)
# 产品
admin.site.register(Product)
# 订单
admin.site.register(Order)
admin.site.register(OrderList)
# 仓库
admin.site.register(Warehouse)
# 库区
admin.site.register(StorageArea)
# 货架
admin.site.register(Shelf)
# 储位
admin.site.register(Storage)
# 进货
admin.site.register(Purchase)
admin.site.register(PurchaseOrder)
# 退货
admin.site.register(Return)
admin.site.register(ReturnOrder)
# 领料
admin.site.register(Production)
admin.site.register(ProductionOrder)
# 退料
admin.site.register(ProductionReturn)
admin.site.register(ProductionReturnOrder)
# 生产
admin.site.register(ProductionReceive)
admin.site.register(ProductionReceiveOrder)
# 销售
admin.site.register(Sale)
admin.site.register(SaleOrder)
# 销退
admin.site.register(SaleReturn)
admin.site.register(SaleReturnOrder)
# 盘点
admin.site.register(InventoryTask)
admin.site.register(InventoryItem)
# 移库
admin.site.register(InventoryMovement)
