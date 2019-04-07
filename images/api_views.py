from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, Http404


from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import (
    FileUploadParser,
    MultiPartParser,
    FormParser
)

from images.models import Image, ImageContainer
from images.serialisers import (
    ImageListSerializer,
    ImageCreateSerializer,
    ImageGetSerializer
)
from worker.tasks import process_image


class ImageList(ListAPIView):
    queryset = ImageContainer.objects.all()
    serializer_class = ImageListSerializer
    permission_classes = (IsAuthenticated, )


class ImageCreate(APIView):
    permission_classes = (IsAuthenticated, )
    parser_classes = (MultiPartParser, )

    def post(self, request, format=None):
        
        submitted_data = ImageCreateSerializer(
            data={"images": request.FILES.values()},
            context={'request': request}
        )
        if not submitted_data.is_valid():
            Response(submitted_data.errors, status=400)

        saved_data = submitted_data.save()

        for uploaded_image_id in saved_data.keys():
            process_image.apply_async((uploaded_image_id, ))

        return Response(saved_data)


class ImageGet(APIView):
    permission_classes = (IsAuthenticated, )

    def get_object(self, pk):
        try:
            return ImageContainer.objects.get(pk=pk)
        except ImageContainer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        img_format = self.request.query_params.get(
            'img_format', 'jpeg')
        
        images = self.get_object(pk).images.exclude(
            img_format__isnull=True).filter(
                img_format=img_format
            )

        if images.exists():
            content_type = "image/{}".format(img_format)
            return HttpResponse(
                images.get().img,
                content_type=content_type
            )
        else:
            return Response({
                "No images of requested format are available "
                "or no images have been processed yet"
            })
