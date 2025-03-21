from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Evento,Chopeira

class CustomUserAdmin(UserAdmin):
    ordering = ['cpf']  # Alterado de 'username' para 'cpf'
    list_display = ('cpf', 'nome', 'email', 'data_nascimento', 'is_active', 'is_staff')
    search_fields = ('cpf', 'nome', 'email')  # Permite busca por CPF, nome ou email

    fieldsets = (
        (None, {'fields': ('cpf', 'password')}),
        ('Informações Pessoais', {'fields': ('nome', 'email', 'data_nascimento')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cpf', 'nome', 'email', 'data_nascimento', 'password1', 'password2'),
        }),
    )

admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Evento)
admin.site.register(Chopeira)