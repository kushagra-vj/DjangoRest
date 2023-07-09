from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user_app.api.serializers import RegistrationSerializer

# comment this when using JWT token authentication mechanism
# from user_app import models # just import where our signal function is defined just to use it internally

@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data['response'] = 'Registration created successfully!'
            data['username'] = account.username
            data['email'] = account.email

            # token = Token.objects.get(user=account).key

            # creating token if not exists for user account
            # token = Token.objects.get_or_create(user=account)
            # data['token'] = token[0].key

            # using simple jwt token authentication to generate token manually
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token)
            }

        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)    