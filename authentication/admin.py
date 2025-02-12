from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Evento

class CustomUserAdmin(UserAdmin):
    # Campos a serem exibidos no formulário de criação de usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','nome','password1', 'password2', 'email'),
        }),
    )

    # Campos a serem exibidos na lista de usuários
    list_display = ('username','nome', 'email','status_pagamento', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'nome')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password','status_pagamento')}),
        ('Personal info', {'fields': ('email','nome')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Evento)