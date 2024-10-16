from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authentication.models import CustomUser
class CustomUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('nome', 'praticas', 'is_staff', 'is_superuser', 'is_active'),
        }),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('praticas',)}),
    )
    list_display = ('username', 'nome', 'email', 'get_praticas', 'is_staff', 'is_superuser', 'is_active')
    
    def get_praticas(self, obj):
        return ", ".join([pratica.nome for pratica in obj.praticas.all()])
    get_praticas.short_description = 'Práticas'

admin.site.register(CustomUser, CustomUserAdmin)
