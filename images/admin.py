from django.contrib import admin

from images.models import Image, ImageContainer


class ImageAdmin(admin.ModelAdmin):
    pass


class ImageContainerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)
admin.site.register(ImageContainer, ImageContainerAdmin)