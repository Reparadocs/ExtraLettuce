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
]

urlpatterns = format_suffix_patterns(urlpatterns)