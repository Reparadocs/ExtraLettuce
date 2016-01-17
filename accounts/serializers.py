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
  token = serializers.CharField(max_length=200)

class BalanceSerializer(serializers.Serializer):
  savings = serializers.IntegerField()

class WithdrawSerializer(serializers.Serializer):
	withdrawal 	= serializers.IntegerField()

class DepositSerializer(serializers.Serializer):
	deposit = serializers.IntegerField()

class IsActiveSerializer(serializers.Serializer):
	active = serializers.BooleanField()

class BankAccountSerializer(serializers.Serializer):
  bank_username = serializers.CharField(max_length=100)
  bank_password = serializers.CharField(max_length=100)
  institution = serializers.CharField(max_length=100)

class BankConfirmSerializer(serializers.Serializer):
  account_id = serializers.CharField(max_length=200)
  token = serializers.CharField(max_length=200)