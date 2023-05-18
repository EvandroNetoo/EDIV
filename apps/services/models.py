from django.db import models
from autenticacao.models import User
from tinymce import models as tynemce_models
from .choices import BudgetStatus, ServiceTags

class Budget(models.Model):
    client = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    data = models.DateTimeField()
    status = models.CharField(max_length=2, choices=BudgetStatus.choices, default=BudgetStatus.SOLICITADO)
    service_tag = models.CharField(max_length=2, choices=ServiceTags.choices)
    descricao = tynemce_models.HTMLField()
    file_path = models.CharField(max_length=36)
