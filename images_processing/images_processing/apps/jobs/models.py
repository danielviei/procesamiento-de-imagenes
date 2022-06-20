import datetime
import logging
import os

from django_fsm import FSMField, transition
from django.db import models
from PIL import Image, ImageOps

db_logger = logging.getLogger('db')

class Jobs(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, null=True, default='PROCESS')

    class Meta:
        ordering = ['id']

class Steps(models.Model):
    job_id = models.ForeignKey(Jobs, on_delete=models.CASCADE, related_name='steps')
    step = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    start_time = models.DateTimeField(default=datetime.datetime.now)
    end_time = models.DateTimeField(default=datetime.datetime.now)

class ImageTransformationFSM(models.Model):
    state = FSMField(default=1)
    image_path = models.FilePathField()
    job_id = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    extension = models.CharField(max_length=5)

    def open_image(self):
        try:
            image = Image.open(self.image_path)
            self.extension = os.path.splitext(self.image_path)[1]
        except Exception as e:
            db_logger.exception(e)
            return None

        return image

    @transition(field=state, source='1', target='2')
    def invert_colors(self):
        try:
            image = self.open_image()
            Steps(
                job_id=self.job_id,
                step="Invertir Colores",
                status="PROCESS",
            ).save()
            
            if self.extension == ".png":
                    inverted_image = ImageOps.invert( image.convert('RGB') )
            else:
                inverted_image = ImageOps.invert(image)

            inverted_image.save(f'./static/{self.job_id.id}/current{self.extension}')
        except Exception as e:
            db_logger.exception(e)
            self.state = 0
            return None

        Steps(
            job_id=self.job_id,
            step="Invertir Colores",
            status="SUCCESS",
        ).save()
            
        db_logger.info(f'Image {self.job_id} had colors inverted')

        return "inverted"

    @transition(field=state, source='2', target='3')
    def to_black_and_white(self):
        try:
            image = self.open_image()
            Steps(
                job_id=self.job_id,
                step="Pasar a Blanco y Negro",
                status="PROCESS",
            ).save()

            b_and_w_image = image.convert("L")
            b_and_w_image.save(f'./static/{self.job_id.id}/current{self.extension}')
        except Exception as e:
            db_logger.exception(e)
            self.state = 0
            return None

        db_logger.info(f'Image {self.job_id} is converted to black and white')
        Steps(
            job_id=self.job_id,
            step="Pasar a Blanco y Negro",
            status="SUCCESS",
        ).save()

        return "black and white"
    
    @transition(field=state, source='3', target='4')
    def rotate(self):
        try:
            image = self.open_image()
            Steps(
                job_id=self.job_id,
                step="Rotar 90 grados",
                status="PROCESS",
            ).save()

            rotate_image = image.rotate(90)
            rotate_image.save(f'./static/{self.job_id.id}/current{self.extension}')
        except Exception as e:
            db_logger.exception(e)
            self.state = 0
            return None

        db_logger.info(f'Image {self.job_id} is rotated 90 degrees')
        
        Steps(
            job_id=self.job_id,
            step="Rotar 90 grados",
            status="SUCCESS",
        ).save()

        return "rotated"

    @transition(field=state, source='4', target='5')
    def invert_vertically(self):
        try:
            image = self.open_image()
            Steps(
                job_id=self.job_id,
                step="Invertir Verticalmente",
                status="PROCESS",
            ).save()

            invert_vertically_image = image.transpose(method=Image.FLIP_TOP_BOTTOM)
            invert_vertically_image.save(f'./static/{self.job_id.id}/current{self.extension}')
        except Exception as e:
            db_logger.exception(e)
            self.state = 0
            return None

        db_logger.info(f'Image {self.job_id} was inverted vertically')
        
        Steps(
            job_id=self.job_id,
            step="Invertir Verticalmente",
            status="SUCCESS",
        ).save()
            
        return "INVERTED VERTICALLY"

    @transition(field=state, source='5', target='0')
    def save_final_image(self):
        try:
            image = self.open_image()
            image.save(f'./static/{self.job_id.id}/final{self.extension}')
        except Exception as e:
            db_logger.exception(e)
            self.state = 0
            return None

        self.job_id.status = "FINISHED"
        self.job_id.save()

        db_logger.info(f'job {self.job_id} is finished')

        return "SAVED"

