import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from bulk_upload.infrastructure.tasks.upload_users_task import import_users_task
from drf_spectacular.utils import extend_schema
from users.application.registration_serializer import RegistrationSerializer

@extend_schema(request=RegistrationSerializer, methods=["POST"])
class UserBulkImportView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        if file.name.endswith('.csv'):
            df = pd.read_csv(file, sep=";")
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            return Response({"error": "File format is not supported"}, status=status.HTTP_400_BAD_REQUEST)

        if len(df) > 20:
            return Response({"error": "Solo se pueden cargar hasta 20 usuarios"}, status=status.HTTP_400_BAD_REQUEST)

        users_data = []
        for _, row in df.iterrows():
            user_data = {
                'username': row.get('username'),
                'password': row.get('password'),
                'email': row.get('email'),
                'role': row.get('role'),
                'first_name': row.get('first_name'),
                'last_name': row.get('last_name'),
                'phone': row.get('phone'),
                'default_address': row.get('default_address'),
                'restaurant': row.get('restaurant')
            }
            users_data.append(user_data)

        import_users_task.apply_async(args=[users_data])

        return Response({"message": "Carga de usuarios iniciada"}, status=status.HTTP_202_ACCEPTED)