from wishlist.models import User, Item, WishList
from django.contrib import admin


class ItemsInline(admin.TabularInline):
    model = Item

class WishListAdmin(admin.ModelAdmin):
    fields = ['name', 'privacy', 'owner', 'members']
    inlines = [ItemsInline]

admin.site.register(User)
admin.site.register(Item)
admin.site.register(WishList, WishListAdmin)