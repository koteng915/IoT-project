from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import DmsSerializer
from .models import Dms
from .admin import admin
import requests
# Create your views here.



class DmsAdmin(admin.ModelAdmin):
    list_display = ('time','distance' )



class DmsViewSet(viewsets.ModelViewSet):
    queryset = Dms.objects.all().order_by('id')
    serializer_class = DmsSerializer
    permission_classes = [permissions.IsAuthenticated]




