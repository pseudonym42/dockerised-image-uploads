from django.db import transaction

from rest_framework import fields
from rest_framework import serializers

from images.models import Image, ImageContainer


class ImageGetSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', )
        model = Image


class ImageListSerializer(serializers.ModelSerializer):
    images = ImageGetSerializer(many=True, read_only=True)

    class Meta:
        model = ImageContainer
        fields = ('id', 'images', )


class ImageCreateSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField(
            allow_empty_file=False,
            use_url=False
        )
    )            
    
    @transaction.atomic
    def create(self, validated_data):

        images = validated_data.pop('images')
        data = {}

        for img in images:
            container = ImageContainer.objects.create(
                created_by=self.context['request'].user
            )
            new_img = Image.objects.create(
                container=container,
                name=img.name,
                img=img
            )
            data[container.id] = {
                'name': img.name
            }

        return data
