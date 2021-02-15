from rest_framework import serializers
from datetime import datetime

from sme_ofertaimoveis.dados_comuns.models import LogFluxoStatus
from sme_ofertaimoveis.users.api.serializers import UserSerializer
from ..serializers.anexo_log_serializer import AnexoLogSerializer

class LogFluxoStatusSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    status_evento_explicacao = serializers.CharField(
        source='get_status_evento_display',
        required=False,
        read_only=True
    )
    data_agendada = serializers.SerializerMethodField('get_format_data')
    anexos = AnexoLogSerializer(many=True, required=False)

    class Meta:
        model = LogFluxoStatus
        fields = ('id', 'status_evento_explicacao', 'usuario', 'anexos', 'criado_em', 'descricao',
                    'justificativa', 'data_agendada', 'email_enviado', 'processo_sei', 'nome_da_unidade')

    def get_format_data(self, obj):
        if obj.data_agendada != None:
            return datetime.strftime(obj.data_agendada, "%Y-%m-%d")
        else:
            return obj.data_agendada
