from django.urls import path
from .views import LoadDataView,CreateSummaryView

urlpatterns = [
    path('loaddata', LoadDataView.as_view(), name='loaddata'),
    path('createsummary', CreateSummaryView.as_view(), name='createsummary'),
]
