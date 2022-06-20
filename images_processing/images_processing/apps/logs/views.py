from django_db_logger.models import StatusLog
from rest_framework import viewsets

from .serializers import LogsSerializer

class LogsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Logs to be viewed or edited.
    """
    queryset = StatusLog.objects.all()
    serializer_class = LogsSerializer
