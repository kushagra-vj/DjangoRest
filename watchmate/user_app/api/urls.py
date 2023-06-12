from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from user_app.api.views import registration_view, logout_view

from rest_framework_simplejwt.views import(
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

urlpatterns = [
    # comment when not using Token Authentication
    path('login/', obtain_auth_token, name='login'),
    path('register/', registration_view, name='registration'),
    path('logout/', logout_view, name='logout'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # to let user verify token validity
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]