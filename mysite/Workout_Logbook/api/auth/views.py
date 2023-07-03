from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import ModifiedTokenObtainPairSerializer, ModifiedTokenRefreshSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase

from ...models import WorkoutUser
from ...utils.api_helpers import get_default_200_response_for_rest_api, get_default_400_response_for_rest_api, \
    google_validate_id_token, facebook_validate_id_token, get_default_404_response_for_rest_api


class ModifiedObtainTokenPairView(TokenObtainPairView):
    """
    Obtém token de acesso para um usuário.
    Viewset aberta (não realiza verificação de acesso por Cliente ou Parceiro)
    """
    permission_classes = (AllowAny,)
    serializer_class = ModifiedTokenObtainPairSerializer


class ModifiedTokenRefreshView(TokenViewBase):
    """
    Refresha um token de acesso para um usuário
    Viewset aberta (não realiza verificação de acesso por Cliente ou Parceiro)
    """
    serializer_class = ModifiedTokenRefreshSerializer


class RegisterView(APIView):
    """
    View para cadastro de novos usuários
    Viewset aberta (não realiza verificação de acesso por Cliente ou Parceiro)
    """
    permission_classes = [AllowAny]

    @transaction.atomic
    def register_new_user(self, data):
        """
            Método atômico pra garantir que sejam criados todos os objetos ou nenhum deles.
        """
        import uuid
        try:
            using_social_network = data.get('socialLogin', False)
            password = str(uuid.uuid4()) if using_social_network else data.get('password')
            user = WorkoutUser.new_user({
                'email': data.get('email'),
                'password': password,
                'first_name': data.get('userFirstName', ''),  # Campo opcional
                'last_name': data.get('userLastName', ''),  # Campo opcional
            })
        except Exception as e:
            print(e)
            return get_default_400_response_for_rest_api()
        return get_default_200_response_for_rest_api()

    def post(self, request):
        return self.register_new_user(request.POST)


class UserRegistrationValidator(APIView):
    """
    Validador de dados de usuário para o momento de cadastro no cliente
    Viewset aberta (não realiza verificação de acesso por Cliente ou Parceiro)
    """
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.POST
        email = data.get('email')
        try:  # Se já existir usuário com o email informado, dá pau
            WorkoutUser.objects.get(email=email)
            return get_default_400_response_for_rest_api(
                {'errors': {'email': _('Usuário com esse endereço de email já existe')}})
        except WorkoutUser.DoesNotExist:
            try:  # Valida o email caso seja inédito
                from django.core.validators import validate_email
                validate_email(email)
            except ValidationError as e:
                return get_default_400_response_for_rest_api({'errors': {'email': e}})
        try:  # Valida a senha
            if not data.get('useSocial',
                            False):  # Se tiver fazendo cadastro com Google/FB não precisa validar senha, pq n tem
                from django.contrib.auth.password_validation import validate_password
                validate_password(data.get('password'))
            return get_default_200_response_for_rest_api()
        except ValidationError as e:
            return get_default_400_response_for_rest_api({'errors': {'password': e}})


class GoogleLoginApi(APIView):
    """
    Pra fazer login com o google, nao precisamos validar email e senha. Precisamos ver se o usuário existe, se o token
    que o Google deu pra ele é válido, e retornar a mesma coisa que a viewset de login retorna caso dê tudo certo.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        pass
        # try:
        #     user = WorkoutUser.objects.get(email=request.POST.get('email'))  # pega user
        #     id_token = request.headers.get('Authorization')
        #     google_validate_id_token(id_token)  # valida token
        #     tokens = TokenObtainPairSerializer.get_token(user)  # retorna access e refred=sh tokens
        #     from rest_framework_simplejwt.settings import api_settings
        #     if api_settings.UPDATE_LAST_LOGIN:  # Atualiza o last login do usuário
        #         from django.contrib.auth.models import update_last_login
        #         update_last_login(None, user)
        #     return get_default_200_response_for_rest_api({'access': str(tokens.access_token), 'refresh': str(tokens)})
        # except WorkoutUser.DoesNotExist as e:
        #     log_error(e)
        #     return get_default_404_response_for_rest_api()
        # except Exception as e:
        #     log_error(e)
        #     return get_default_400_response_for_rest_api()


class FacebookLoginApi(APIView):
    """
    Pra fazer login com o meta, nao precisamos validar email e senha. Precisamos ver se o usuário existe, se o token
    que o Google deu pra ele é válido, e retornar a mesma coisa que a viewset de login retorna caso dê tudo certo.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        pass
        # try:
        #     user = WorkoutUser.objects.get(email=request.POST.get('email'))  # pega user
        #     id_token = request.headers.get('Authorization')
        #     facebook_validate_id_token(id_token)  # valida token
        #     tokens = TokenObtainPairSerializer.get_token(user)  # retorna access e refred=sh tokens
        #     from rest_framework_simplejwt.settings import api_settings
        #     if api_settings.UPDATE_LAST_LOGIN:  # Atualiza o last login do usuário
        #         from django.contrib.auth.models import update_last_login
        #         update_last_login(None, user)
        #     return get_default_200_response_for_rest_api({'access': str(tokens.access_token), 'refresh': str(tokens)})
        # except WorkoutUser.DoesNotExist as e:
        #     log_error(e)
        #     return get_default_404_response_for_rest_api()
        # except Exception as e:
        #     log_error(e)
        #     return get_default_400_response_for_rest_api()
