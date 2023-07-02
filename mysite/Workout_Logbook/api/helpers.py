from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _


def get_custom_action_not_allowed_http_code_and_message():
    """
    Retorna o código HTTP e mensagem customizados pra quando o usuário tenta realizar uma ação num objeto que não é seu
    """
    return {'message': _('Permission denied!'), 'code': 408}


def get_request_user(request):
    """
    Retorna o usuário da requisicao
    """
    if request.user:
        return request.user.id
    return request.headers['user']


def default_list(viewset, request, *args, **kwargs):
    """
    Lógica de override do método list das viewsets de listagem de objetos.
    Realiza o filtro de acordo com o modelo dos objetos do atributo queryset da viewset passada como parâmetro.
    Utiliza o método get_queryset implementado no modelo pra pegar a queryset, e pagina os objetos normal, de acordo com
    o método list padrao do DRF.
    """
    queryset = viewset.filter_queryset(
        viewset.get_queryset().model.get_queryset(get_request_user(request), *args, **kwargs))
    # viewset.get_queryset retorna uma queryset. queryset.model retorna o modelo dos seus objetos. model.get_queryset
    # retorna a queryset de objetos, filtrada de maneira correta pelo modelo.
    page = viewset.paginate_queryset(queryset)
    if page is not None:
        serializer = viewset.get_serializer(page, many=True)
        return viewset.get_paginated_response(serializer.data)

    serializer = viewset.get_serializer(queryset, many=True)
    return Response(serializer.data)


def default_retrieve(self, request, *args, **kwargs):
    """
    Override do método delete do mixin do DRF pra verificar se o usuário tem permissão de ver o objeto desejado
    """
    instance = self.get_object()
    owner_id = instance.owner_id()
    if owner_id and owner_id != get_request_user(request):
        self.permission_denied(
            request,
            **get_custom_action_not_allowed_http_code_and_message()
        )
    serializer = self.get_serializer(instance)
    return Response(serializer.data)


def default_create(self, request, *args, **kwargs):
    """
    Override do método delete do mixin do DRF pra verificar se o usuário tem permissão de criar o objeto desejado
    """
    instance = self.get_object()
    owner_id = instance.owner_id()
    if owner_id and owner_id != get_request_user(request):
        self.permission_denied(
            request,
            **get_custom_action_not_allowed_http_code_and_message()
        )
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


def default_update(self, request, *args, **kwargs):
    """
    Override do método delete do mixin do DRF pra verificar se o usuário tem permissão de editar o objeto desejado
    """
    instance = self.get_object()
    owner_id = instance.owner_id()
    if owner_id and owner_id != get_request_user(request):
        self.permission_denied(
            request,
            **get_custom_action_not_allowed_http_code_and_message()
        )
    partial = kwargs.pop('partial', False)
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)

    if getattr(instance, '_prefetched_objects_cache', None):
        # If 'prefetch_related' has been applied to a queryset, we need to
        # forcibly invalidate the prefetch cache on the instance.
        instance._prefetched_objects_cache = {}

    return Response(serializer.data)


def default_delete(self, request, *args, **kwargs):
    """
    Override do método delete do mixin do DRF pra verificar se o usuário tem permissão de apagar o objeto desejado
    """
    instance = self.get_object()
    owner_id = instance.owner_id()
    if owner_id and owner_id != get_request_user(request):
        self.permission_denied(
            request,
            **get_custom_action_not_allowed_http_code_and_message()
        )
    return self.destroy(request, *args, **kwargs)


class CustomListAPIView(generics.ListAPIView):
    """
    Override de ListAPIView para verificação de permissão do usuário
    """

    def list(self, request, *args, **kwargs):
        """
        Garante que serão listados apenas objetos do Cliente desejado
        """
        return default_list(self, request, *args, **kwargs)


class CustomListCreateAPIView(generics.ListCreateAPIView):
    """
    Override de ListCreateAPIView para verificação de permissão do usuário
    """

    def list(self, request, *args, **kwargs):
        """
        Garante que serão listados apenas objetos do Cliente desejado
        """
        return default_list(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """ Verifica se o parceiro logado tem permissão de criação
        """
        return default_create(self, request, *args, **kwargs)


class CustomRetrieveAPIView(generics.RetrieveAPIView):
    """
    Override de RetrieveAPIView para verificação de permissão do usuário
    """

    def retrieve(self, request, *args, **kwargs):
        return default_retrieve(self, request, *args, **kwargs)


class CustomUpdateAPIView(generics.UpdateAPIView):
    """
    Override de UpdateAPIView para verificação de permissão do usuário
    """

    def update(self, request, *args, **kwargs):
        return default_update(self, request, *args, **kwargs)


class CustomDestroyAPIView(generics.DestroyAPIView):
    """
    Override de DestroyAPIView para verificação de permissão do usuário
    """

    def delete(self, request, *args, **kwargs):
        return default_delete(self, request, *args, **kwargs)


class CustomRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Override de RetrieveUpdateAPIView para verificação de permissão do usuário
    """

    def retrieve(self, request, *args, **kwargs):
        return default_retrieve(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return default_update(self, request, *args, **kwargs)


class CustomRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    """
    Override de RetrieveDestroyAPIView para verificação de permissão do usuário
    """

    def retrieve(self, request, *args, **kwargs):
        return default_retrieve(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return default_delete(self, request, *args, **kwargs)


class CustomRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Override de RetrieveUpdateDestroyAPIView para verificação de permissão do usuário
    """

    def retrieve(self, request, *args, **kwargs):
        return default_retrieve(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return default_update(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return default_delete(self, request, *args, **kwargs)


class CustomModelViewSet(viewsets.ModelViewSet):
    """
    Override de CustomModelViewSet para verificação de permissão do usuário em todas as ações
    """

    def create(self, request, *args, **kwargs):
        return default_create(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return default_retrieve(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return default_update(self, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return default_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return default_delete(self, request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return default_list(self, request, *args, **kwargs)
