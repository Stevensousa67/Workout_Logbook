from django.db import models


class BaseModel(models.Model):

    class Meta:
        abstract = True

    @classmethod
    def get_queryset(cls, user_id):
        """
        Deve ser implementado por cada classe-filha. Implementa a lógica de filtragem com base no usuário (cada usuário
        só vê o que lhe pertence)
        """
        return

    def owner_id(self):
        """
        Retorna o id do usuário dono do objeto
        """
        return
