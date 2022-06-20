import os

from django.shortcuts import render
from PIL import Image
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from images_processing.apps.jobs.tasks import start_fsm
from .models import Jobs, Steps, ImageTransformationFSM
from .serializers import JobSerializer, StepSerializer

class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Jobs to be viewed or edited.
    """
    queryset = Jobs.objects.all()
    serializer_class = JobSerializer

class StepViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Steps to be viewed or edited.
    """
    queryset = Steps.objects.all()
    serializer_class = StepSerializer


from django import forms

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

        serializer = JobSerializer(data=body)

        if serializer.is_valid():
            serializer.save()

            image = Image.open(request.FILES["image"])
            
            extension = os.path.splitext(str(request.FILES["image"]))[1]
            os.makedirs(f'./static/{serializer.data["id"]}')

            image.save(f'./static/{serializer.data["id"]}/original{extension}')
            image.save(f'./static/{serializer.data["id"]}/current{extension}')

            job=Jobs.objects.get(id=serializer.data["id"])

            fsm = ImageTransformationFSM(
                image_path=f'./static/{serializer.data["id"]}/current{extension}',
                job_id=job,
                extension=extension,
            )

            fsm.save()
            start_fsm.delay(fsm.id)

            return Response(serializer.data["id"], status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

