import os
from django.http import FileResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from reports.domain.models import SalesReport
from reports.infrastructure.tasks.task import generate_sales_report
from drf_spectacular.utils import extend_schema


@extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "month": {""},
                "year": {""},
            },
        },
    },
    methods=["POST"],
)
class GenerateSalesReportView(APIView):
    def post(self, request):
        month = request.data.get("month")
        year = request.data.get("year")

        report = SalesReport.objects.create(month=month, year=year)
        generate_sales_report.delay(report.id, month, year)

        return Response({"report_id": str(report.id)}, status=status.HTTP_202_ACCEPTED)


@extend_schema(
    request={},
    methods=["GET"],
)
class DownloadReportView(APIView):
    def get(self, request, report_id):
        report = SalesReport.objects.filter(id=report_id, status="ok").first()
        if not report or not report.file_path or not os.path.exists(report.file_path):
            raise Http404("El archivo aun no ha sido generado.")

        response = FileResponse(open(report.file_path, "rb"), as_attachment=True)
        os.remove(report.file_path)
        report.delete()
        return response
