from django.contrib import admin
from .models import Category, Subcategory, Expert

class SubcategoryInline(admin.TabularInline):
    model = Subcategory

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        SubcategoryInline,
    ]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory)
admin.site.register(Expert)


from django.contrib import admin
from .models import Owner

admin.site.register(Owner)
