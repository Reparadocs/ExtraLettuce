from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import *
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from accounts.serializers import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_swagger import *
from django.core.mail import send_mail
from datetime import date
import requests
import json

class CreateAccount(APIView):
  def post(self, request, format=None):
    """
    Create an account. Returns 201 upon successful creation, and 400 for already
    existing user or for any other bad request.
    ---
    request_serializer: RegistrationSerializer
    response_serializer: RegistrationSerializer
    """
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
    """
    Set an amount of money to save at a set frequency.
    Returns 200 upon success and 400 on error.
    ---
    request_serializer: ScheduleSerializer
    """
    serializer = ScheduleSerializer(data=request.data)
    if serializer.is_valid():
      request.user.scheduled_deposit = serializer.data['amount']
      frequency = serializer.data['frequency']
      request.user.scheduled_frequency = frequency
      if frequency == "day":
        request.user.scheduled_days_left = 1
      elif frequency == "week":
        request.user.scheduled_days_left = 7
      elif frequency == "month":
        request.user.scheduled_days_left = 30
      request.user.save()
      return Response({'success': True}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScheduleDaysLeft(APIView):
  authentication_classes = (TokenAuthentication, SessionAuthentication)
  permission_classes = (IsAuthenticated,)

  def get(self, request, format=None):
    """
    Retrieve the days left for the deposit cycle.
    ---
    response_serializer: ScheduleDaysLeftSerializer
    """
    return Response(ScheduleDaysLeftSerializer(request.user).data)

class AccountInfo(APIView):
  authentication_classes = (TokenAuthentication, SessionAuthentication)
  permission_classes = (IsAuthenticated,)

  def get(self, request, format=None):
    """
    Retrieve the account information.
    Returns 200 upon success.
    ---
    response_serializer: AccountSerializer
    """
    return Response(AccountSerializer(request.user).data)

class AccountBalanceInfo(APIView):
  authentication_classes = (TokenAuthentication, SessionAuthentication)
  permission_classes = (IsAuthenticated,)

  def get(self, request, format=None):
    """
    Retrieve the account's balance information.
    Returns 200 upon success.
    ---
    response_serializer: BalanceSerializer
    """
    return Response(BalanceSerializer(request.user).data)

class AccountWithdraw(APIView):
  authentication_classes = (TokenAuthentication, SessionAuthentication)
  permission_classes = (IsAuthenticated,)

  def post(self, request, format=None):
    """
    Withdraw from the account's savings.
    Returns 200 upon success and 400 on withdrawing amount greater than
    the total savings or for any other bad request.
    ---
    request_serializer: WithdrawSerializer
    """
    serializer = WithdrawSerializer(data=request.data)
    if serializer.is_valid():
      withdrawal = serializer.data['withdrawal']
      if withdrawal > request.user.savings: # withdrawing amount more than savings
        return Response({'errors': 'Withdrawing amount greater than total savings'}, status=status.HTTP_400_BAD_REQUEST)
      request.user.savings = request.user.savings - withdrawal
      request.user.save()
      history = History(date=date.today(), balance=request.user.savings, owner=request.user)
      history.save()
      return Response({'success': True}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountDeposit(APIView):
  authentication_classes = (TokenAuthentication, SessionAuthentication)
  permission_classes = (IsAuthenticated,)

  def post(self, request, format=None):
    """
    Deposit into the account's savings. Every deposit will
    also be logged in the acouunt's balance history.
    Returns 200 upon success and 400 on error.
    ---
    request_serializer: DepositSerializer
    """
    serializer = DepositSerializer(data=request.data)
    if serializer.is_valid():
      deposit = serializer.data['deposit']
      if deposit > request.user.bank_amount: #depositing more than bank amount
        return Response({'errors': 'Depositing more than bank amount'}, status=status.HTTP_400_BAD_REQUEST)
      request.user.savings = request.user.savings + deposit
      request.user.bank_amount = request.user.bank_amount - deposit
      request.user.save()
      history = History(date=date.today(), balance=request.user.savings, owner=request.user)
      history.save()
      return Response({'success': True}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountIsActive(APIView):
  authentication_classes = (TokenAuthentication, SessionAuthentication)
  permission_classes = (IsAuthenticated,)

  def get(self, request, format=None):
    """
    Query whether or not the account is saving money
    at the specified frequency.
    ---
    response_serializer: IsActiveSerializer
    """
    return Response(IsActiveSerializer(request.user).data)

class AccountRestart(APIView):
  authentication_classes = (TokenAuthentication, SessionAuthentication)
  permission_classes = (IsAuthenticated,)

  def get(self, request, format=None):
    """
    Sets the active status of the account to true.
    Returns 200 upon success and 400 if account is already active.
    ---
    response_serializer: ScheduleSerializer
    """
    if request.user.active: #error if already active
      return Response({'errors': 'Already active'}, status=status.HTTP_400_BAD_REQUEST)
    request.user.active = True
    request.user.save()
    return Response({'success': True}, status=status.HTTP_200_OK)

class AccountPause(APIView):
  authentication_classes = (TokenAuthentication, SessionAuthentication)
  permission_classes = (IsAuthenticated,)

  def get(self, request, format=None):
    """
    Sets the active status of the account to false.
    Returns 200 upon success and 400 if account is already inactive.
    ---
    response_serializer: ScheduleSerializer
    """
    if not(request.user.active): #error if already active
      return Response({'errors': 'Already not active'}, status=status.HTTP_400_BAD_REQUEST)
    request.user.active = False
    request.user.save()
    return Response({'success': True}, status=status.HTTP_200_OK)

class AccountLink(APIView):
  authentication_classes = (TokenAuthentication, SessionAuthentication)
  permission_classes = (IsAuthenticated,)

  def post(self, request, format=None):
    """
    Links the account to the given bank account.
    Returns 200 upon success and 400 on error.
    ---
    request_serializer: BankAccountSerializer
    """
    serializer = BankAccountSerializer(data=request.data)
    if serializer.is_valid():
      payload = {
        'public_key': '67393c180257916a023493c5adc0d3',
        'username': serializer.data['bank_username'],
        'password': serializer.data['bank_password'],
        'institution_type': serializer.data['institution'],
        'product': 'auth',
        'include_accounts': True,
      }
      r = requests.post("https://link-tartan.plaid.com/authenticate", data=payload)
      response = r.json()
      if r.status_code != 200:
        return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
      else:
        accounts = []
        for account in response['accounts']:
          accounts.append({
            'balance': account['balance']['current'],
            'id': account['_id'],
            'name': account['meta']['name']
          })
        result = {'accounts': accounts, 'token': response['public_token']}
        return Response(json.dumps(result), status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountMock(APIView):
  authentication_classes = (TokenAuthentication, SessionAuthentication)
  permission_classes = (IsAuthenticated,)

  def get(self, request, format=None):
    """
    Retrieve the account bank information.
    ---
    response_serializer: BankMockSerializer
    """
    return Response(BankMockSerializer(request.user).data)

  def post(self, request, format=None):
    """
    Update user's bank amount and bank name.
    Returns 200 upon success and 400 on error.
    ---
    request_serializer: BankMockSerializer
    """
    serializer = BankMockSerializer(data=request.data)
    if serializer.is_valid():
      request.user.bank_amount = serializer.data['bank_amount']
      request.user.bank_name = serializer.data['bank_name']
      request.user.save()
      return Response({'success': True}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountConfirm(APIView):
  authentication_classes = (TokenAuthentication, SessionAuthentication)
  permission_classes = (IsAuthenticated,)

  def post(self, request, format=None):
    """
    Confirms the given account.
    Returns 200 upon success and 400 on error.
    ---
    request_serializer: BankConfirmSerializer
    """
    serializer = BankConfirmSerializer(data=request.data)
    if serializer.is_valid():
      payload = {
        'client_id': '569ab81ba4ce3935462bb607',
        'secret': '973fdf467c57fc885fbd631a5653bd',
        'public_token': serializer.data['token'],
        'account_id': serializer.data['account_id'],
      }
      r = requests.post("https://tartan.plaid.com/exchange_token", data=payload)
      response = r.json()
      if r.status_code != 200:
        return Response(r.json(), status=status.HTTP_400_BAD_REQUEST)
      else:
        request.user.token = response['stripe_bank_account_token']
        request.user.save()
        return Response({'success': True}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountGoals(APIView):
  authentication_classes = (TokenAuthentication, SessionAuthentication)
  permission_classes = (IsAuthenticated,)

  def get(self, request, format=None):
    """
    Retrieves the specified goal.
    Returns 200 upon success and 400 on error.
    ---
    response_serializer: AccountGoalSerializer
    """
    if len(request.user.goal_set.all()) is not 0:
      return Response(AccountGoalSerializer(request.user.goal_set.all(), many=True).data)
    return Response({})

  def post(self, request, format=None):
    """
    Updates the specified goal.
    Returns 201 upon success and 400 on error.
    """
    serializer = AccountGoalSerializer(data=request.data)
    if serializer.is_valid():
      goal = Goal(name=serializer.data['name'], amount=serializer.data['amount'], owner=request.user)
      goal.save()
      return Response({"success": True}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountHistory(APIView):
  authentication_classes = (TokenAuthentication, SessionAuthentication)
  permission_classes = (IsAuthenticated,)

  def get(self, request, format=None):
    """
    Retrieves the savings balance history with corresponding date and times.
    ---
    response_serializer: AccountHistorySerializer
    """
    return Response(AccountHistorySerializer(request.user.history_set.all(), many=True).data)

class DailyCron(APIView):
  def post(self, request, format=None):
    send_mail('Test Cron', 'Here is a test', 'reparadocs@amazon.com', ['reparadocs@gmail.com'])

class DeleteHistory(APIView):
  def get(self, request, format=None):
    request.user.history_set.all().delete()
    request.user.save()
    return Response(AccountHistorySerializer(request.user.history_set.all(), many=True).data)

class HistoryMock1(APIView): # d,d,d,d,d
  def get(self, request, format=None):
    request.user.savings = 100000
    request.user.scheduled_deposit = 20000
    request.user.scheduled_frequency = 'week'
    request.user.active = True
    request.user.bank_amount = 9000000
    request.user.bank_name = 'Bank of America'
    request.user.save()
    history = History(date="2015-12-20", balance=20000, owner=request.user)
    history.save()
    history = History(date="2015-12-27", balance=40000, owner=request.user)
    history.save()
    history = History(date="2016-1-3",   balance=60000, owner=request.user)
    history.save()
    history = History(date="2015-1-10",  balance=80000, owner=request.user)
    history.save()
    goal = Goal(name='Trip to France', amount=1600000, owner=request.user)
    goal.save()
    return Response(AccountHistorySerializer(request.user.history_set.all(), many=True).data)

class HistoryMock2(APIView): # d,d,w,d,w
  def get(self, request, format=None):
    request.user.savings = 40000
    request.user.scheduled_deposit = 20000
    request.user.scheduled_frequency = 'week'
    request.user.active = True
    request.user.bank_amount = 9000000
    request.user.bank_name = 'Bank of America'
    request.user.save()
    history = History(date="2015-12-20", balance=20000, owner=request.user)
    history.save()
    history = History(date="2015-12-27", balance=40000, owner=request.user)
    history.save()
    history = History(date="2016-1-3",   balance=30000, owner=request.user)
    history.save()
    history = History(date="2015-1-10",  balance=50000, owner=request.user)
    history.save()
    goal = Goal(name='Trip to France', amount=1600000, owner=request.user)
    goal.save()
    return Response(AccountHistorySerializer(request.user.history_set.all(), many=True).data)

class HistoryMock3(APIView): # d,d,w,d,d
  def get(self, request, format=None):
    request.user.savings = 50000
    request.user.scheduled_deposit = 20000
    request.user.scheduled_frequency = 'week'
    request.user.active = True
    request.user.bank_amount = 9000000
    request.user.bank_name = 'Bank of America'
    request.user.save()
    history = History(date="2015-12-20", balance=20000, owner=request.user)
    history.save()
    history = History(date="2015-12-27", balance=40000, owner=request.user)
    history.save()
    history = History(date="2016-1-3",   balance=10000, owner=request.user)
    history.save()
    history = History(date="2015-1-10",  balance=30000, owner=request.user)
    history.save()
    goal = Goal(name='Trip to France', amount=1600000, owner=request.user)
    goal.save()
    return Response(AccountHistorySerializer(request.user.history_set.all(), many=True).data)

class HistoryMock4(APIView): # d,d,d,d,w
  def get(self, request, format=None):
    request.user.savings = 50000
    request.user.scheduled_deposit = 20000
    request.user.scheduled_frequency = 'week'
    request.user.active = True
    request.user.bank_amount = 9000000
    request.user.bank_name = 'Bank of America'
    request.user.save()
    history = History(date="2015-12-20", balance=20000, owner=request.user)
    history.save()
    history = History(date="2015-12-27", balance=40000, owner=request.user)
    history.save()
    history = History(date="2016-1-3",   balance=60000, owner=request.user)
    history.save()
    history = History(date="2015-1-10",  balance=80000, owner=request.user)
    history.save()
    goal = Goal(name='Trip to France', amount=1600000, owner=request.user)
    goal.save()
    return Response(AccountHistorySerializer(request.user.history_set.all(), many=True).data)

# account history mocks
# d,d,d,d,d,d,d,d,d,d,d
# d,d,d,w,w,d,w,d,d,w,d
# d,w,d,w,d,w,d,d,w,d,d