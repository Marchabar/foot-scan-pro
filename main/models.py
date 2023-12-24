from django.db import models

class Equipo (models.Model):
    id_equipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    logo = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']

class Jugador (models.Model):
    id_jugador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    edad = models.IntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre', 'edad']

class Partido (models.Model):
    id_partido = models.AutoField(primary_key=True)
    equipo_local = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='equipo_local')
    equipo_visitante = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='equipo_visitante')
    goles_local = models.IntegerField()
    goles_visitante = models.IntegerField()
    fecha = models.DateField()

    def __str__(self):
        return str(self.equipo_local) + ' vs ' + str(self.equipo_visitante)

    class Meta:
        ordering = ['fecha', 'equipo_local', 'equipo_visitante']

class Jornada (models.Model):
    id_jornada = models.AutoField(primary_key=True)
    numero = models.IntegerField(unique=True)
    partidos = models.ForeignKey(Partido, on_delete=models.CASCADE)
    fecha = models.DateField()

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['numero']