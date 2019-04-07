import uuid

from django.db import models
from django.contrib.auth import get_user_model


def get_img_path(instance, filename):
    return 'files/user_{user}/{hash}/{name}'.format(
        user=instance.container.created_by.id,
        hash=str(uuid.uuid4()),
        name=filename
    )

class ImageContainer(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.CASCADE)


class Image(models.Model):
    container = models.ForeignKey(ImageContainer,
                                  on_delete=models.CASCADE,
                                  related_name='images')
    name = models.CharField(max_length=256)
    img = models.ImageField(upload_to=get_img_path)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    img_format = models.CharField(max_length=64, null=True)

    def __str__(self):
        return self.name