from django.urls import path

from service.views import Events, VoteView, Account

urlpatterns = [
    path('account/<int:pk>/', Account.as_view(), name='account'),
    path('events/', Events.as_view({'get': 'list', 'post': 'create'}), name='events'),
    path('events/<int:pk>/', Events.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='events'),
    path('events/<int:pk>/vote', VoteView.as_view(), name='vote')
]