from django.urls import path

from reports.infrastructure.http.reports_controller import DownloadReportView, GenerateSalesReportView

urlpatterns = [
    path('generate-report', GenerateSalesReportView.as_view(), name='sales-report-view'),
    path('download/<uuid:report_id>', DownloadReportView.as_view(), name='download-and-destroy')
]