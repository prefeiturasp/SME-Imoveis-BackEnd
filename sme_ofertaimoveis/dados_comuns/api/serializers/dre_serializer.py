from rest_framework import serializers

from ...models import DiretoriaRegional


class DreSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiretoriaRegional
        fields = '__all__'
