from datetime import date
from functools import cmp_to_key
from django.db.models import fields
from rest_framework import serializers
from metro.models import  Metro

class MetroDetailSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Metro
        fields = '__all__'

