from django.http.response import HttpResponse
from core.models import Notification, Document
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import (
   NotificationModelSerializer,
   DocumentModelSerializer,
)

from django.core.files.storage import FileSystemStorage


class UserNotificationList(generics.ListAPIView):
    """
       List all Notifications based on the auth user
    """
    serializer_class = NotificationModelSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self, *args, **kwargs):
        try:
            qs = Notification.objects.filter(to_user=self.request.user).order_by("-updated")
            read = self.request.GET.get("read")
            if read and read=='yes':
                qs = qs.filter(read=True)
            if read and read=='no':
                qs = qs.filter(read=False)
            status_code = status.HTTP_200_OK
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs



class UserNotificationDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a Notification
    """
    serializer_class = NotificationModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()
    lookup_field = "pk"



class UserNotificationDeleteAPIView(generics.DestroyAPIView):
    """
       Allows destroy of Noticiation
    """
    serializer_class = NotificationModelSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Notification.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        dta = {"detail": "Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)


class UserNotificationUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of parts or all Notifiaction
    """
    serializer_class = NotificationModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()
    lookup_field = "pk"



class DocumentList(generics.ListAPIView):
    """
       List all Documents based on the auth user
    """
    serializer_class = DocumentModelSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self, *args, **kwargs):
        try:
            qs = Document.objects.all().order_by("-updated")
            allow_download = self.request.GET.get("allow_download")
            if allow_download and allow_download=='yes':
                qs = qs.filter(allow_download=True)
            if allow_download and allow_download=='no':
                qs = qs.filter(allow_download=False)
            status_code = status.HTTP_200_OK
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs



class DocumentDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a Document
    """
    serializer_class = DocumentModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Document.objects.all()
    lookup_field = "pk"


class DocumentDownloadAPIView(APIView):
    """
       Allow Document Download
    """
    serializer_class = DocumentModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    # queryset = Document.objects.all()
    # lookup_field = "pk"
    # def get(self, request, format="json"):
    def get(self, request, *args, **kwargs):
        # 
        try:
            uid = kwargs.get('uid',)
            try:
                document = Document.objects.get(uid=uid)
            except Document.DoesNotExist as exp:
                document = Document.objects.latest("updated")
            except Exception as exp:
                print(exp)
                raise ValidationError({"detail": f"Client Error: {exp}"})

            # finally:
            file_path = document.document.path
            file_title = document.title
            print(file_path)
            print(file_title)
            with open(file_path, 'rb') as excel_file:
                response = HttpResponse(excel_file, content_type='application/vnd.ms-excel')
                filename = f"{file_title}.xlsx"
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
        except Exception as exp:
            raise ValidationError({"detail": f"Client Error: {exp}"})


class DocumentUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of parts or all Notifiaction
    """
    serializer_class = DocumentModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Document.objects.all()
    lookup_field = "pk"


class DocumentDeleteAPIView(generics.DestroyAPIView):
    """
       Allows destroy of Noticiation
    """
    serializer_class = DocumentModelSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Document.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        dta = {"detail": "Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)

