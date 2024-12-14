from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.domain.models import User


class UserController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        users = User.objects.all()
        data = [{"id": user.id} for user in users]
        return Response(data)