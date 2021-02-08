from rest_framework import serializers
from datetime import datetime

from sme_ofertaimoveis.dados_comuns.models import AnexoLog, LogFluxoStatus

class AnexoLogSerializer(serializers.ModelSerializer):
    get_tipo_documento_display = serializers.CharField(required=False)

    def validate_arquivo(self, arquivo):
        filesize = arquivo.size

        if filesize > 10485760:
            raise ValidationError("O tamanho máximo de arquivos é 10MB")
        else:
            return arquivo

    def create(self, validated_data):
        log_id = validated_data.get('log').id
        log = LogFluxoStatus.objects.get(id=log_id)
        arquivo = validated_data.get('arquivo')
        tipo_documento = validated_data.get('tipo_documento')
        nome = validated_data.get('nome')
        anexo = AnexoLog.objects.create(log=log, arquivo=arquivo,
                                        tipo_documento=tipo_documento, nome=nome)
        return anexo

    class Meta:
        model = AnexoLog
        exclude = ("id",)
