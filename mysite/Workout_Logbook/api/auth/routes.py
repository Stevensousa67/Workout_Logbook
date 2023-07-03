from django.urls import path
from .views import ModifiedObtainTokenPairView, RegisterView, ModifiedTokenRefreshView, UserRegistrationValidator, \
    GoogleLoginApi, FacebookLoginApi

router = [
    path('auth/login/', ModifiedObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', ModifiedTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/validate-user/', UserRegistrationValidator.as_view(), name='validate_user'),
    path('auth/google-login/', GoogleLoginApi.as_view(), name='google-login'),
    path('auth/facebook-login/', FacebookLoginApi.as_view(), name='google-login'),
]
