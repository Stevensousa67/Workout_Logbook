from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10


def get_custom_action_not_allowed_http_code_and_message() -> dict:
    """ Retorna o código HTTP e mensagem customizados pra quando o cliente tem acesso à feature mas o parceiro não tem
    permissão pra realizar a ação
    """
    return {'message': _('Você não tem permissão para fazer isso!'), 'code': 408}


def get_custom_feature_blocked_http_code_and_message() -> dict:
    """ Retorna o código HTTP e mensagem customizados pra quando o cliente não tem acesso à feature
    """
    return {'message': _('O conteúdo desejado não está incluso no seu plano atual.'), 'code': 407}


def google_validate_id_token(token: str) -> None:
    """
    Valida o token do google passado pelo cliente. Se validar, pode logar o usuário
    """
    pass
    # from google.oauth2 import id_token
    # from google.auth.transport import requests
    # # a partir de idinfo da pra pegar informaccoes do usuario pra cadastro, como nome, foto, etc
    # idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_OAUTH2_CLIENT_ID)


def facebook_validate_id_token(token: str) -> None:
    """
    Valida o token do facebook passado pelo cliente. Se validar, pode logar o usuário
    """
    pass
    # import requests
    # url = f'https://graph.facebook.com/oauth/access_token?client_id={FACEBOOK_CLIENT_ID}&client_secret={FACEBOOK_CLIENT_SECRET}&grant_type=client_credentials'
    # app_token_response = requests.get(url)
    # app_token_json = app_token_response.json()
    # app_token = app_token_json.get('access_token')
    # if not app_token:
    #     raise Exception(app_token_json.get('error', {'message': 'Fatal error!!'}).get('message'))
    # url2 = f'https://graph.facebook.com/debug_token?input_token={token}&access_token={app_token}'
    # valid_token_response = requests.get(url2)
    # valid_token_response_json = valid_token_response.json()
    # if not valid_token_response_json.get('data', {}).get('is_valid', False):
    #     raise Exception(
    #         valid_token_response_json.get('data', {'error': {'message': 'Token fatal error!!'}}).get('error', {
    #             'message': 'Token fatal error!!'}).get('message'))


def get_default_response_for_rest_api(http_status: int, data: dict = None, header: dict = None) -> Response:
    """
    Retorna a response padrão para requisicoes do Django Rest
    """
    if data is None:
        data = {}
    return Response(data, status=http_status, headers=header)


def get_default_200_response_for_rest_api(data: dict = None) -> Response:
    if data is None:
        data = {'msg': _('Sucesso')}
    return get_default_response_for_rest_api(status.HTTP_200_OK, data)


def get_default_201_response_for_rest_api(data: dict = None) -> Response:
    if data is None:
        data = {'msg': _('Sucesso')}
    return get_default_response_for_rest_api(status.HTTP_201_CREATED, data)


def get_default_400_response_for_rest_api(data: dict = None) -> Response:
    if data is None:
        data = {'msg': _('Ocorreu um erro. Por favor, contacte o suporte.')}
    return get_default_response_for_rest_api(status.HTTP_400_BAD_REQUEST, data)


def get_default_404_response_for_rest_api(data: dict = None) -> Response:
    if data is None:
        data = {'msg': _('Conteúdo não encontrado.')}
    return get_default_response_for_rest_api(status.HTTP_404_NOT_FOUND, data)
