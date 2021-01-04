from rest_framework import serializers

from sme_ofertaimoveis.dados_comuns.models import LogFluxoStatus
from sme_ofertaimoveis.users.api.serializers import UserSerializer


class LogFluxoStatusSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    status_evento_explicacao = serializers.CharField(
        source='get_status_evento_display',
        required=False,
        read_only=True
    )

    class Meta:
        model = LogFluxoStatus
        fields = ('status_evento_explicacao', 'usuario', 'criado_em', 'descricao', 'justificativa')
