from rest_framework import serializers
from .models import*
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']

# Student Profile Serializer
# Scholarship Serializer
class ScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = '__all__'

from rest_framework import serializers
from .models import ScholarshipApplication

class ScholarshipApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScholarshipApplication
        fields = '__all__'
        read_only_fields = ['student', 'application_date']