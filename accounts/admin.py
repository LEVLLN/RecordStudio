from django.contrib import admin
from . import models


@admin.register(models.SecretHashCode)
class SecretHashCodeAdmin(admin.ModelAdmin):
    pass
