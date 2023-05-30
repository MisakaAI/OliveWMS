from django.contrib import admin
from .models import *

# 管理页面顶部的文字
admin.site.site_header = "Olive WMS"
#  <title> （字符串）末尾放置的文字。
admin.site.site_title = 'Olive WMS'
# 管理索引页顶部的文字（一个字符串）
admin.site.index_title = "又不是不能用的仓储管理系统"

# 供应商
admin.site.register(supplier)
# 仓库
admin.site.register(warehouse)
# 库区
admin.site.register(storage_area)
# 储位
admin.site.register(storage_location)

# 进货单
admin.site.register(Purchase)

# 货架
@admin.register(shelf)
class shelfAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'storage_area', 'max_row', 'max_column')
    search_fields = ('name',)

# 产品
@admin.register(item)
class itemAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'price')
    search_fields = ('name',)
