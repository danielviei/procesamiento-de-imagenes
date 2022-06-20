from django_db_logger.models import StatusLog
from rest_framework import generics

from .serializers import LogsSerializer

class LogsListAPIView(generics.ListAPIView):
    """
    API endpoint that allows Logs to be viewed.
    """
    serializer_class = LogsSerializer

    def get_queryset(self):
        queryset = StatusLog.objects.all()
        min_date = self.request.query_params.get('min_date')
        if min_date is not None:
            queryset = queryset.filter(create_datetime__gte=min_date)
        max_date = self.request.query_params.get('max_date')
        if max_date is not None:
            queryset = queryset.filter(create_datetime__lte=max_date)
        return queryset

class LogsRetrieveAPIView(generics.RetrieveAPIView):
    """
    API endpoint that returns a Logs object.
    """
    queryset = StatusLog.objects.all()
    serializer_class = LogsSerializer
    lookup_field = 'id'