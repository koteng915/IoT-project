from rest_framework import serializers
from .models import Dms



class DmsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dms
        fields = ('time','distance')

