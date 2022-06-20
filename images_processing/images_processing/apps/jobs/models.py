import datetime
import os

from django_fsm import FSMField, transition
from django.db import models
from PIL import Image, ImageOps

class Jobs(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, null=True)

class Steps(models.Model):
    job_id = models.ForeignKey(Jobs, on_delete=models.CASCADE)
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
        image = Image.open(self.image_path)
        self.extension = os.path.splitext(self.image_path)[1]

        return image
    
    @transition(field=state, source='1', target='2')
    def invert_colors(self):
        image = self.open_image()

        if self.extension == ".png":
                inverted_image = ImageOps.invert( image.convert('RGB') )
        else:
            inverted_image = ImageOps.invert(image)

        inverted_image.save(f'./static/{self.job_id.id}/current{self.extension}')

        return "inverted"

    @transition(field=state, source='2', target='3')
    def to_black_and_white(self):
        image = self.open_image()

        b_and_w_image = image.convert("L")
        b_and_w_image.save(f'./static/{self.job_id.id}/current{self.extension}')

        return "black and white"
    
    @transition(field=state, source='3', target='4')
    def rotate(self):
        image = self.open_image()

        rotate_image = image.rotate(90)
        rotate_image.save(f'./static/{self.job_id.id}/current{self.extension}')

        return "rotated"

    @transition(field=state, source='4', target='5')
    def invert_vertically(self):
        image = self.open_image()

        invert_vertically_image = image.transpose(method=Image.FLIP_TOP_BOTTOM)
        invert_vertically_image.save(f'./static/{self.job_id.id}/current{self.extension}')


    @transition(field=state, source='5', target='0')
    def save_final_image(self):
        image = self.open_image()
        image.save(f'./static/{self.job_id.id}/final{self.extension}')

