from django.urls import path

from bulk_upload.infrastructure.http.upload_controller import UserBulkImportView

urlpatterns = [
    path('users', UserBulkImportView.as_view(), name='bulk-import-users'),
]