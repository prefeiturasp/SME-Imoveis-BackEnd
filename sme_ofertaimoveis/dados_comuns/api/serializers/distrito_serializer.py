from rest_framework import serializers

from ...models import Distrito


class DistritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distrito
        fields = '__all__'
