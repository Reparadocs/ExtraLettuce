from django.conf.urls import include, url
from rest_framework.authtoken import views as authviews
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^create/', views.CreateAccount.as_view(), name='create'),
    url(r'^schedule/', views.ScheduleAccount.as_view(), name='schedule'),
    url(r'^info/', views.AccountInfo.as_view(), name='info'),
    url(r'^balance/', views.AccountBalanceInfo.as_view(), name='balance'),
    url(r'^withdraw/', views.AccountWithdraw.as_view(), name='withdraw'),
    url(r'^deposit/', views.AccountDeposit.as_view(), name='deposit'),
    url(r'^active/', views.AccountIsActive.as_view(), name='active'),
    url(r'^restart/', views.AccountRestart.as_view(), name='restart'),
    url(r'^pause/', views.AccountPause.as_view(), name='pause'),
    url(r'^link/', views.AccountLink.as_view(), name='link'),
    url(r'^confirm/', views.AccountConfirm.as_view(), name='confirm'),
    url(r'^mock/', views.AccountMock.as_view(), name='mock'),
    url(r'^goals/', views.AccountGoals.as_view(), name='goals'),
    url(r'^days/', views.ScheduleDaysLeft.as_view(), name='days'),
    url(r'^history/', views.AccountHistory.as_view(), name='history'),
    url(r'^daily/', views.DailyCron.as_view(), name='daily'),
    url(r'^historymock1/', views.HistoryMock1.as_view(), name='historymock1'),
    url(r'^historymock2/', views.HistoryMock2.as_view(), name='historymock2'),
    url(r'^historymock3/', views.HistoryMock3.as_view(), name='historymock3'),
    url(r'^historymock4/', views.HistoryMock4.as_view(), name='historymock4'),
    url(r'^clearhistory/', views.DeleteHistory.as_view(), name='clearhistory'),
]

urlpatterns = format_suffix_patterns(urlpatterns)