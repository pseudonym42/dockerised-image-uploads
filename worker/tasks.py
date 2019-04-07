import os
import subprocess

from worker.worker import app
from django.conf import settings

from images.models import ImageContainer


@app.task(bind=True)
def process_image(self, obj_id):

    instance = ImageContainer.objects.get(pk=obj_id)
    original_image = instance.images.get()

    process_data = subprocess.run(
        [
            'identify {}'.format(original_image.img.path)
        ],
        shell=True,
        check=True,
        stdout=subprocess.PIPE
    ).stdout.decode("UTF-8")

    print(process_data)

    invalid_file_format = all([
        "JPEG" not in process_data,
        "PNG" not in process_data
    ])

    if invalid_file_format:
        print("Invalid file format")
        return

    if 'JPEG' in process_data:
        new_file_format = 'png'
        original_image.img_format = 'jpeg'
    elif 'PNG' in process_data:
        new_file_format = 'jpeg'
        original_image.img_format = 'png'

    original_image.save(update_fields=["img_format"])

    new_file_name = "converted_img.{}".format(new_file_format)
    new_img_path = original_image.img.path.split(
        original_image.name)[0] + new_file_name

    subprocess.run(
        [
            'cp {original} {copy} && convert {copy} {copy}'.format(
                original=original_image.img.path,
                copy=new_img_path
            )
        ],
        shell=True,
        check=True,
        stdout=subprocess.PIPE
    )

    duplicate = instance.images.get()
    duplicate.id = None
    duplicate.img_format = new_file_format
    duplicate.img.name = new_img_path
    duplicate.name = new_file_name
    duplicate.save()
   
