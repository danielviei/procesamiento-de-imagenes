import logging
import os

from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from images_processing.apps.jobs.tasks import start_fsm
from .models import Jobs, ImageTransformationFSM
from .serializers import JobSerializer

class JobsListAPIView(generics.ListAPIView):
    """
    API endpoint that returns a list of jobs paginated.
    """
    queryset = Jobs.objects.all()
    serializer_class = JobSerializer

class JobsRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    API endpoint that returns a job object.
    """
    queryset = Jobs.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        if request.data["step"] < 1 or request.data["step"] > 4:
            db_logger = logging.getLogger('db')
            db_logger.error("Step debe tener un valor entre [1, 4]")
            return HttpResponse({"ERROR": "Step debe tener un valor entre [1, 4]"}, status_code=status.HTTP_400_BAD_REQUEST)

        fsm = ImageTransformationFSM(
            job_id=self.get_object(),
        )

        self.get_object().status = "PROCESS"

        fsm.save()
        start_fsm.delay(fsm.id)

        res = self.update(request, *args, **kwargs)
        
        return res 

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

@api_view(['GET', 'POST'])
def job_start(request):
    """
    Create a new Job
    """
    if request.method == 'GET':
        form = UploadFileForm()
        return render(request, 'upload.html', {'form': form})

    if request.method == 'POST':
        body = request.data
        body["step"] = 1

        serializer = JobSerializer(data=body)

        if serializer.is_valid():
            serializer.save()

            image = Image.open(request.FILES["image"])
            
            extension = os.path.splitext(str(request.FILES["image"]))[1]
            os.makedirs(f'./static/{serializer.data["id"]}', exist_ok=True)

            image.save(f'./static/{serializer.data["id"]}/original{extension}')
            image.save(f'./static/{serializer.data["id"]}/current{extension}')

            job=Jobs.objects.get(id=serializer.data["id"])
            job.path_image = f'./static/{serializer.data["id"]}/current{extension}'
            job.save()

            fsm = ImageTransformationFSM(job_id=job)

            fsm.save()
            start_fsm.delay(fsm.id)

            return Response(serializer.data["id"], status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

