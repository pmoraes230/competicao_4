from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=45)
    cpf = models.CharField(max_length=14)
    email = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'cliente'
        
    def __str__(self):
        return self.nome

class Evento(models.Model):
    nome = models.CharField(max_length=45)
    dia = models.DateField()
    horario = models.TimeField(unique=True)
    cpt_evento = models.IntegerField()
    preco = models.CharField(max_length=45)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)
    imagem = models.ImageField(upload_to="event", blank=False, null=False)
    descricao = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'evento'

    def __str__(self):
        return self.nome

class Ingresso(models.Model):
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING)
    evento = models.ForeignKey(Evento, models.DO_NOTHING)
    setor = models.ForeignKey('Setor', models.DO_NOTHING)
    id_ingresso = models.CharField(primary_key=True, max_length=45)
    data_emissao = models.DateTimeField()
    valor = models.CharField(max_length=45)
    status_ingresso = models.CharField(db_column='status_Ingresso', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ingresso'
        
    def __str__(self):
        return f"Ingresso cliente {self.cliente}"


class Perfil(models.Model):
    nome = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'perfil'
        
    def __str__(self):
        return self.nome

class Setor(models.Model):
    nome = models.CharField(max_length=45)
    qtd_setor = models.IntegerField()
    evento = models.ForeignKey(Evento, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'setor'
        
    def __str__(self):
        return self.nome


class Usuario(models.Model):
    nome = models.CharField(max_length=45)
    email = models.CharField(unique=True, max_length=45)
    cpf = models.CharField(unique=True, max_length=14)
    senha = models.CharField(unique=True, max_length=340)
    perfil = models.ForeignKey(Perfil, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'usuario'

    def __str__(self):
        return self.nome