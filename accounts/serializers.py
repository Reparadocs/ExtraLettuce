from rest_framework import serializers
from accounts.models import Account

class RegistrationSerializer(serializers.Serializer):
  username = serializers.CharField(max_length=100)
  password = serializers.CharField(max_length=100)

class ScheduleSerializer(serializers.Serializer):
  amount = serializers.IntegerField()
  frequency = serializers.ChoiceField(choices=['day', 'week', 'month'])

class AccountSerializer(serializers.Serializer):
  username = serializers.CharField(max_length=100)
  scheduled_deposit = serializers.IntegerField()
  savings = serializers.IntegerField()
  scheduled_frequency = serializers.ChoiceField(choices=['day', 'week', 'month'])

