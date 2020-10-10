from django.contrib import admin

from backend.pasta.models import *


admin.site.register(Unit)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(MetadataProduct)
admin.site.register(Amount)
admin.site.register(CommandPasta)