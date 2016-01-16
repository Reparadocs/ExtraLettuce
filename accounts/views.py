from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import Account
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from accounts.serializers import RegistrationSerializer, ScheduleSerializer, AccountSerializer, BalanceSerializer, WithdrawSerializer, DepositSerializer
from django.core.exceptions import ObjectDoesNotExist

class CreateAccount(APIView):
  def post(self, request, format=None):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
      try:
        account = Account.objects.get(username=serializer.data['username'])
      except ObjectDoesNotExist:
        account = Account.objects.create_user(
          serializer.data['username'],
          '',
          serializer.data['password']
        )
        token = Token.objects.create(user=account)
        print token
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
      return Response({'errors': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScheduleAccount(APIView):
  authentication_classes = (TokenAuthentication, SessionAuthentication)
  permission_classes = (IsAuthenticated,)

  def post(self, request, format=None):
    serializer = ScheduleSerializer(data=request.data)
    if serializer.is_valid():
      request.user.scheduled_deposit = serializer.data['amount']
      request.user.scheduled_frequency = serializer.data['frequency']
      request.user.save()
      return Response({'success': True}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountInfo(APIView):
  authentication_classes = (TokenAuthentication, SessionAuthentication)
  permission_classes = (IsAuthenticated,)

  def get(self, request, format=None):
    return Response(AccountSerializer(request.user).data)

class AccountBalanceInfo(APIView):
  authentication_classes = (TokenAuthentication, SessionAuthentication)
  permission_classes = (IsAuthenticated,)

  def get(self, request, format=None):
    return Response(BalanceSerializer(request.user).data)

class AccountWithdraw(APIView):
  authentication_classes = (TokenAuthentication, SessionAuthentication)
  permission_classes = (IsAuthenticated,)

  def post(self, request, format=None):
    serializer = WithdrawSerializer(data=request.data)
    if serializer.is_valid():
      withdrawal = serializer.data['withdrawal']
      if withdrawal > request.user.savings: # withdrawing amount more than savings
        return Response({'errors': 'Withdrawing amount greater than total savings'}, status=status.HTTP_400_BAD_REQUEST)
      request.user.savings = request.user.savings - withdrawal
      request.user.save()
      return Response({'success': True}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountDeposit(APIView):
  authentication_classes = (TokenAuthentication, SessionAuthentication)
  permission_classes = (IsAuthenticated,)

  def post(self, request, format=None):
    serializer = DepositSerializer(data=request.data)
    if serializer.is_valid():
      request.user.savings = request.user.savings + serializer.data['deposit']
      request.user.save()
      return Response({'success': True}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

