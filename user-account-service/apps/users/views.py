from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from apps.users.documents import UserDocument
from apps.users.serializers import UserSerializer
from utils import Response
from utils.permissions import IsAdmin

User = get_user_model()


class UserView(generics.GenericAPIView):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "is_active",
                openapi.IN_QUERY,
                description="Filter users by active status",
                type=openapi.TYPE_BOOLEAN,
            ),
            openapi.Parameter(
                "email",
                openapi.IN_QUERY,
                description="Filter users by email",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "nin",
                openapi.IN_QUERY,
                description="Filter users by national identification number",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "phone",
                openapi.IN_QUERY,
                description="Filter users by phone number",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        is_active = request.GET.get("is_active", False)
        email = request.GET.get("email", "")
        nin = request.GET.get("nin", "")
        phone = request.GET.get("phone", "")

        if not any([is_active, email, nin, phone]):
            users = self.get_queryset()
        else:
            user_search = UserDocument.search()

            if is_active:
                user_search = user_search.filter("term", is_active=is_active)
            if phone:
                user_search = user_search.filter("match_phrase", phone=phone)
            if email:
                user_search = user_search.filter("match_phrase", email=email)
            if nin:
                user_search = user_search.filter("match_phrase", nin=nin)

            response = user_search.execute()
            user_ids = [hit.meta.id for hit in response]
            users = self.get_queryset().filter(id__in=user_ids)

        serializer = self.get_serializer(users, many=True)

        return Response(
            message="Users returned successfully",
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self):
        user_id = self.kwargs.get("user_id")
        obj = self.model.objects.filter(id=user_id).first()
        if not obj:
            raise NotFound("User not found")
        return obj

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)

        return Response(
            message="User returned", data=serializer.data, status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            message="User updated", data=serializer.data, status=status.HTTP_200_OK
        )

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            message="User updated", data=serializer.data, status=status.HTTP_200_OK
        )
