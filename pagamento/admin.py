from django.contrib import admin
from django.db.models import Sum
from .models import Transacao

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('transacao_id', 'usuario', 'data_transacao', 'valor_total', 'status')  # Campos exibidos na lista
    list_filter = (
        ('data_transacao', admin.DateFieldListFilter),  # Filtro por dia, mês e ano
        'status',  # Filtro por status
    )
    search_fields = ('transacao_id', 'usuario__username')  # Permite buscar pelo ID da transação ou nome do usuário

    def changelist_view(self, request, extra_context=None):
        # Calcula a soma total das transações filtradas
        queryset = self.get_queryset(request)
        total = queryset.aggregate(total=Sum('valor_total'))['total'] or 0

        # Adiciona o total ao contexto
        extra_context = extra_context or {}
        extra_context['total_transacoes'] = total

        return super().changelist_view(request, extra_context=extra_context)

    def get_changelist(self, request, **kwargs):
        """
        Sobrescreve o changelist para exibir o total no rodapé.
        """
        from django.contrib.admin.views.main import ChangeList

        class CustomChangeList(ChangeList):
            def get_results(self, *args, **kwargs):
                super().get_results(*args, **kwargs)
                # Adiciona o total ao rodapé
                self.total_transacoes = self.result_list.aggregate(total=Sum('valor_total'))['total'] or 0

        return CustomChangeList