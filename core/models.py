from time import timezone
from django.db import models

# BaseModels para adicionar campos de data de criação, atualização e exclusão lógica
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    # Soft delete criado para marcar o registro como excluído sem removê-lo do banco de dados
    def delete( self, using=None, keep_parents=False):
        self.is_deleted = True
        self.delete_at = timezone.now()
        self.save()