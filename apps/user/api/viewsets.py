from django.contrib.auth import login, logout
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from restdoctor.rest_framework import viewsets

from apps.user.api.serializers import RegistrationSerializer, UserSerializer, LoginSerializer
from apps.user.dto.authenticate import LoginDto
from apps.user.logic.facades.user import user__registration
from apps.user.logic.interactors.stream_key import stream_key__decode
from apps.user.logic.interactors.user import user__generate_stream_key, user__authenticate
from apps.user.models import User
from apps.widget_settings.api.serializers import WidgetSettingsPydanticSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes_map = {
        'default': [permissions.IsAuthenticated],
        'login': [permissions.AllowAny],
        'registration': [permissions.AllowAny],
        'logout': [permissions.IsAuthenticated],
        'auth': [permissions.AllowAny]
    }
    serializer_class_map = {
        'default': UserSerializer,
        'registration': {
            'request': RegistrationSerializer
        },
        'login': {
            'request': LoginSerializer
        },
        'settings': {
            'request': WidgetSettingsPydanticSerializer
        }
    }

    @action(detail=False, methods=['post'])
    def registration(self, request: Request) -> Response:
        request_serializer = self.get_request_serializer(
            data=request.data
        )
        request_serializer.is_valid(raise_exception=True)
        user, stream_key = user__registration(
            validated_data=request_serializer.pydantic_instance
        )
        login(request, user)
        response_serializer = self.get_response_serializer(instance=user)
        return Response(
            response_serializer.data, headers={
                'Set-Cookie': f"stream_key={stream_key}; Path=/; Same-site=Lax"
            }
        )

    @action(detail=False, methods=['post'])
    def login(self, request: Request) -> Response:
        request_serializer = self.get_request_serializer(data=request.data)
        request_serializer.is_valid(raise_exception=False)
        user = user__authenticate(
            login_dto=LoginDto(
                username=request_serializer.data.get('username'),
                password=request_serializer.data.get('password'),
            )
        )
        login(request, user)
        stream_key = user__generate_stream_key(user=user)
        response_serializer = self.get_response_serializer(
            instance=user
        )
        return Response(
            data=response_serializer.data,
            headers={
                'access-control-expose-headers': 'Set-Cookie',
                'Set-Cookie': f"stream_key={stream_key}; Path=/; Same-site=Lax",
            }
        )

    @action(detail=False, methods=['post'])
    def logout(self, request: Request) -> Response:
        logout(request)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def auth(self, request: Request) -> Response:
        key = request.data.get('key')
        user = stream_key__decode(key=key)
        if user:
            return Response(status=200)
        return Response(status=401)

    @action(detail=False, methods=['get'])
    def me(self, request: Request) -> Response:
        return Response(self.get_response_serializer(instance=request.user).data, status=status.HTTP_200_OK)



        # @action(detail=True, methods=['get'])
        # def get_chunk(self, request: Request, client_id: typing.Any) -> Response:
        #     global some_dict[client_id] = stream_id
        #     data = requests.get(f'http://127.0.0.1:8000/hls/{chank_id}').data
        #     return Response(data)
