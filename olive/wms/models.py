from django.db import models
from datetime import datetime

# 仓库
class warehouse(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='名称')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name='仓库'
        verbose_name_plural='仓库'

# 库区
class storage_area(models.Model):
    name = models.CharField(max_length=20, verbose_name='名称')
    warehouse = models.ForeignKey('warehouse', on_delete=models.CASCADE, verbose_name='所属仓库')

    def __str__(self) -> str:
        return '[' + self.warehouse.name + '] ' + self.name

    class Meta:
        verbose_name='库区'
        verbose_name_plural='库区'
        unique_together = ('warehouse', 'name')

# 货架
class shelf(models.Model):
    storage_area = models.ForeignKey('storage_area', on_delete=models.CASCADE, verbose_name='库区')
    name = models.CharField(max_length=20, verbose_name='名称')
    max_row = models.PositiveSmallIntegerField(default=4, verbose_name='层数')
    max_column = models.PositiveSmallIntegerField(default=6, verbose_name='每层储位数')

    def __str__(self) -> str:
        return '[' + self.storage_area.warehouse.name + "|" + self.storage_area.name + '] ' + self.name

    class Meta:
        verbose_name='货架'
        verbose_name_plural='货架'
        unique_together = ('storage_area', 'name')

# 储位
class storage_location(models.Model):
    shelf = models.ForeignKey('shelf', on_delete=models.CASCADE, verbose_name='货架')
    row = models.PositiveSmallIntegerField(verbose_name='行')
    column = models.PositiveSmallIntegerField(verbose_name='列')
    item = models.CharField(max_length=20, verbose_name='物品')
    quantity = models.PositiveIntegerField(verbose_name='数量')
    def __str__(self) -> str:
        return str(self.shelf.id) + "-" + str(self.row) + "-" + str(self.column)

    class Meta:
        verbose_name='储位'
        verbose_name_plural='储位'

# 产品
class item(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='名称')
    unit = models.CharField(max_length=10, default='个', verbose_name='单位')
    price = models.IntegerField(null=True, blank=True, verbose_name='价格')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name='产品'
        verbose_name_plural='产品'

# 供应商
class supplier(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='名称')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name='供应商'
        verbose_name_plural='供应商'

# 进货
class Purchase(models.Model):
    serial = models.PositiveSmallIntegerField(verbose_name='序号')
    createtime = models.DateTimeField(auto_now_add=True)
    supplier = models.CharField(max_length=20, verbose_name='供应商')
    item_list = models.JSONField(default=list, blank=True, verbose_name='清单')

    def __str__(self) -> str:
        return self.createtime.strftime("%Y%m%d") + str(self.serial).zfill(4)

    class Meta:
        verbose_name='进货单'
        verbose_name_plural='进货单'
#     #当天日期+流水号
#     class CustomID(models.PositiveBigIntegerField):
#         def __init__(self, *args, **kwargs):
#             kwargs.setdefault('editable', False)
#             kwargs.setdefault('unique', True)
#             kwargs.setdefault('primary_key', True)
#             super().__init__(*args, **kwargs)

#         def generate_next_value(self):
#             today = datetime.today().strftime('%Y%m%d')
#             last_id = self.model.objects.order_by('id').last()
#             if not last_id:
#                 return int(today + '0001')
#             else:
#                 last_id = str(last_id.id)
#                 date_part, serial_part = last_id[:-4], last_id[-4:]
#                 if date_part == today:
#                     serial_part = str(int(serial_part) + 1).zfill(4)
#                 else:
#                     serial_part = '0001'
#                 return int(today + serial_part)
#     

#     def __str__(self) -> str:
#         return self.id

# # 退货
# class Return(models.Model):
#     pass

# # 生产领料
# class Production_Receive(models.Model):
#     pass

# # 生产退料
# class Production_Return(models.Model):
#     pass

# # 生产入库
# class Production_Storage(models.Model):
#     pass

# # 销售
# class Sale(models.Model):
#     pass
# # 销退
# class Sales_Return(models.Model):
#     pass
