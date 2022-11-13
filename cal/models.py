from email.policy import default
from tabnanny import verbose
from django.db import models


class CalDia(models.Model):
    """A model for daily information"""
    
    class FarmaciaDeServico(models.TextChoices):
        PISCO = 'Pisco'
        ROLDAO = 'Roldão'
        CRUZ_F = 'Cruz Ferreira'
        GIL = 'Gil'
        MATILDE_S = 'Matilde Soares'
        LAURA_A_L = 'Laura A. Leite'
        NENHUMA = '-'
        DO_EXCEL = '0'

    day = models.DateField(unique=True)
    fds_excel = models.CharField(max_length=20, blank=True, null=True)
    info = models.CharField(verbose_name="Mais info", max_length=30, blank=True, null=True)
    farmacia_de_servico = models.CharField(
        verbose_name="Farmácia",
        max_length=20,
        choices=FarmaciaDeServico.choices,
        default=FarmaciaDeServico.DO_EXCEL,
    )

    def __str__(self) -> str:
        return self.day.strftime("%Y%m%d")

