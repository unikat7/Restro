from django.contrib import admin
from .models import Category, MenuItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'is_special', 'is_vegetarian')
    list_filter = ('category', 'is_available', 'is_special', 'is_vegetarian')
    list_editable = ('price', 'is_available', 'is_special')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
