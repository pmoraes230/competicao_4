from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Cliente)
admin.site.register(models.Evento)
admin.site.register(models.Ingresso)
admin.site.register(models.Perfil)
admin.site.register(models.Setor)
admin.site.register(models.Usuario)