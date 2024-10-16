from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Mantém os campos padrão do Django e adiciona as práticas no formulário de criação de usuário
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('praticas', 'is_staff', 'is_superuser', 'is_active'),  # Adiciona staff, superuser e ativo
        }),
    )

    # Mantém os campos padrão e adiciona as práticas no formulário de alteração de usuário
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('praticas',)}),  # Agrupando todos os campos adicionais em um único tuple
    )

    # Campos a serem exibidos na lista de usuários
    list_display = ('username', 'email', 'get_praticas', 'is_staff', 'is_superuser', 'is_active')

    # Busca por campos específicos no admin
    search_fields = ('username', 'email', 'praticas__nome')

    # Para exibir as práticas na listagem de usuários
    def get_praticas(self, obj):
        return ", ".join([pratica.nome for pratica in obj.praticas.all()])

    get_praticas.short_description = 'Práticas'

admin.site.register(CustomUser, CustomUserAdmin)
