from django.db import models


# 供应商
class Supplier(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "供应商"
        verbose_name_plural = "供应商"


# 产品
class Product(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="名称")
    unit = models.CharField(max_length=10, default="个", verbose_name="单位")
    price = models.IntegerField(null=True, blank=True, verbose_name="单价")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "产品"
        verbose_name_plural = "产品"


# 订单
class Order(models.Model):
    serial = models.PositiveSmallIntegerField(verbose_name="序号")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    customer = models.CharField(max_length=20, verbose_name="客户名称")
    STATUS_CHOICES = [
        ("wait", "待生产"),
        ("production", "生产中"),
        ("completed", "生产完"),
        ("sendout", "已发货"),
        ("finished", "完成"),
        ("no", "未完成"),
        ("cancelled", "取消"),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, verbose_name="状态"
    )


# 订单列表
class OrderList(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="订单")
    oid = models.PositiveSmallIntegerField(verbose_name="序号")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="产品")
    quantity = models.PositiveIntegerField(default=0, verbose_name="数量")
    price = models.IntegerField(null=True, blank=True, verbose_name="单价")


# 仓库
class Warehouse(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "仓库"
        verbose_name_plural = "仓库"


# 库区
class StorageArea(models.Model):
    name = models.CharField(max_length=20, verbose_name="名称")
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, verbose_name="所属仓库"
    )

    def __str__(self):
        return f"[{self.warehouse.name}]{self.name}"

    class Meta:
        verbose_name = "库区"
        verbose_name_plural = "库区"
        unique_together = ("warehouse", "name")


# 货架
class Shelf(models.Model):
    storage_area = models.ForeignKey(
        StorageArea, on_delete=models.CASCADE, verbose_name="库区"
    )
    name = models.CharField(max_length=20, verbose_name="名称")
    max_row = models.PositiveSmallIntegerField(default=4, verbose_name="层数")
    max_column = models.PositiveSmallIntegerField(default=6, verbose_name="每层储位数")

    def __str__(self):
        return (
            f"[{self.storage_area.warehouse.name}|{self.storage_area.name}]{self.name}"
        )

    class Meta:
        verbose_name = "货架"
        verbose_name_plural = "货架"
        unique_together = ("storage_area", "name")


# 储位
class Storage(models.Model):
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE, verbose_name="货架")
    row = models.PositiveSmallIntegerField(verbose_name="行")
    column = models.PositiveSmallIntegerField(verbose_name="列")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="产品")
    quantity = models.PositiveIntegerField(default=0, verbose_name="数量")
    enable = models.BooleanField(default=True, verbose_name="启用")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return f"{self.shelf.name}-{str(self.row)}-{str(self.column)}"

    class Meta:
        verbose_name = "储位"
        verbose_name_plural = "储位"
        unique_together = ("shelf", "row", "column")


# 进货
class Purchase(models.Model):
    serial = models.PositiveSmallIntegerField(verbose_name="序号")
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="供应商",
    )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return f"P{self.created_time.strftime('%Y%m%d')}{str(self.serial).zfill(4)}"

    class Meta:
        verbose_name = "进货"
        verbose_name_plural = "进货"
        unique_together = ("serial", "created_time")


class PurchaseOrder(models.Model):
    pid = models.ForeignKey(Purchase, on_delete=models.CASCADE, verbose_name="单号")
    serial = models.PositiveSmallIntegerField(verbose_name="序号")
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, verbose_name="储位")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="产品")
    quantity = models.PositiveIntegerField(default=0, verbose_name="数量")
    price = models.IntegerField(null=True, blank=True, verbose_name="单价")


# 退货
class Return(models.Model):
    serial = models.PositiveSmallIntegerField(verbose_name="序号")
    purchase = models.ForeignKey(
        Purchase, on_delete=models.CASCADE, verbose_name="进货单"
    )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return f"R{self.created_time.strftime('%Y%m%d')}{str(self.serial).zfill(4)}"

    class Meta:
        verbose_name = "退货"
        verbose_name_plural = "退货"
        unique_together = ("serial", "created_time")


class ReturnOrder(models.Model):
    pid = models.ForeignKey(Return, on_delete=models.CASCADE, verbose_name="单号")
    serial = models.PositiveSmallIntegerField(verbose_name="序号")
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, verbose_name="储位")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="产品")
    quantity = models.PositiveIntegerField(default=0, verbose_name="数量")
    price = models.IntegerField(null=True, blank=True, verbose_name="单价")


# 领料
class Production(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="订单")
    serial = models.PositiveSmallIntegerField(verbose_name="序号")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return f"R{self.created_time.strftime('%Y%m%d')}{str(self.serial).zfill(4)}"

    class Meta:
        verbose_name = "领料出库"
        verbose_name_plural = "领料出库"
        unique_together = ("serial", "created_time")


class ProductionOrder(models.Model):
    pid = models.ForeignKey(Production, on_delete=models.CASCADE, verbose_name="单号")
    serial = models.PositiveSmallIntegerField(verbose_name="序号")
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, verbose_name="储位")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="产品")
    quantity = models.PositiveIntegerField(default=0, verbose_name="数量")


# 退料
class ProductionReturn(models.Model):
    production = models.ForeignKey(
        Production, on_delete=models.CASCADE, verbose_name="生产领料"
    )
    serial = models.PositiveSmallIntegerField(verbose_name="序号")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return f"R{self.created_time.strftime('%Y%m%d')}{str(self.serial).zfill(4)}"

    class Meta:
        verbose_name = "退料入库"
        verbose_name_plural = "退料入库"
        unique_together = ("serial", "created_time")


class ProductionReturnOrder(models.Model):
    pid = models.ForeignKey(
        ProductionReturn, on_delete=models.CASCADE, verbose_name="单号"
    )
    serial = models.PositiveSmallIntegerField(verbose_name="序号")
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, verbose_name="储位")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="产品")
    quantity = models.PositiveIntegerField(default=0, verbose_name="数量")


# 生产
class ProductionReceive(models.Model):
    production = models.ForeignKey(
        Production, on_delete=models.CASCADE, verbose_name="生产领料"
    )
    STATUS_CHOICES = [
        ("finished", "成品"),
        ("semi", "半成品"),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, verbose_name="状态"
    )
    serial = models.PositiveSmallIntegerField(verbose_name="序号")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return f"R{self.created_time.strftime('%Y%m%d')}{str(self.serial).zfill(4)}"

    class Meta:
        verbose_name = "生产入库"
        verbose_name_plural = "生产入库"
        unique_together = ("serial", "created_time")


class ProductionReceiveOrder(models.Model):
    pid = models.ForeignKey(
        ProductionReceive, on_delete=models.CASCADE, verbose_name="单号"
    )
    serial = models.PositiveSmallIntegerField(verbose_name="序号")
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, verbose_name="储位")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="产品")
    quantity = models.PositiveIntegerField(default=0, verbose_name="数量")


# 销售
class Sale(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="订单")
    serial = models.PositiveSmallIntegerField(verbose_name="序号")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return f"R{self.created_time.strftime('%Y%m%d')}{str(self.serial).zfill(4)}"

    class Meta:
        verbose_name = "销售"
        verbose_name_plural = "销售"
        unique_together = ("serial", "created_time")


class SaleOrder(models.Model):
    pid = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name="单号")
    serial = models.PositiveSmallIntegerField(verbose_name="序号")
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, verbose_name="储位")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="产品")
    quantity = models.PositiveIntegerField(default=0, verbose_name="数量")
    price = models.IntegerField(null=True, blank=True, verbose_name="单价")


# 销退
class SaleReturn(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name="销售单")
    serial = models.PositiveSmallIntegerField(verbose_name="序号")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return f"SR{self.created_time.strftime('%Y%m%d')}{str(self.serial).zfill(4)}"

    class Meta:
        verbose_name = "销退"
        verbose_name_plural = "销退"
        unique_together = ("serial", "created_time")


class SaleReturnOrder(models.Model):
    pid = models.ForeignKey(SaleReturn, on_delete=models.CASCADE, verbose_name="单号")
    serial = models.PositiveSmallIntegerField(verbose_name="序号")
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, verbose_name="储位")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="产品")
    quantity = models.PositiveIntegerField(default=0, verbose_name="数量")
    price = models.IntegerField(null=True, blank=True, verbose_name="单价")


# 盘点
class InventoryTask(models.Model):
    serial = models.PositiveSmallIntegerField(verbose_name="序号")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="仓库",
    )
    STATUS_CHOICES = [
        ("wait", "待开始"),
        ("progress", "进行中"),
        ("completed", "已完成"),
        ("cancelled", "已取消"),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="状态"
    )

    def __str__(self):
        return f"PD{self.created_time.strftime('%Y%m%d')}{str(self.serial).zfill(4)}"

    class Meta:
        verbose_name = "盘点"
        verbose_name_plural = "盘点"
        unique_together = ("serial", "created_time")


# 盘点清单
class InventoryItem(models.Model):
    task = models.ForeignKey(
        InventoryTask, on_delete=models.CASCADE, verbose_name="盘点任务"
    )
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, verbose_name="储位")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="产品")
    system_quantity = models.PositiveIntegerField(verbose_name="系统数量")
    actual_quantity = models.PositiveIntegerField(default=0, verbose_name="实际数量")
    status = models.BooleanField(default=False, verbose_name="状态")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")


# 库存移动历史
class InventoryMovement(models.Model):
    TRANSACTION_TYPES = [
        ("Purchase", "进货"),
        ("Return", "退货"),
        ("Production", "领料"),
        ("ProductionReturn", "退料"),
        ("ProductionReceive", "生产"),
        ("Sale", "销售")("SaleReturn", "销退")("Inventory", "盘点")("Move", "移库"),
    ]
    transaction = models.CharField(
        max_length=20, choices=TRANSACTION_TYPES, verbose_name="事务"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="产品")
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, verbose_name="储位")
    quantity = models.IntegerField(verbose_name="数量变更")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "库存移动历史"
        verbose_name_plural = "库存移动历史"

    def __str__(self):
        action = "入库" if self.quantity > 0 else "出库"
        return f"{self.get_transaction_display()}-{self.product.name}({abs(self.quantity)}) {action}"
