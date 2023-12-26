from django.db import models


class Equipo (models.Model):
    id_equipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    logo = models.URLField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']

class Jugador (models.Model):
    id_jugador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    edad = models.IntegerField()
    dorsal = models.IntegerField()
    posicion = models.CharField(max_length=15, choices=[('Portero', 'Portero'), ('Defensa', 'Defensa'), ('Centrocampista', 'Centrocampista'), ('Delantero', 'Delantero')])
    nacionalidad = models.URLField(null=True, blank=True)
    foto = models.URLField(null=True, blank=True)

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
    jornada = models.ForeignKey('Jornada', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.equipo_local) + ' vs ' + str(self.equipo_visitante)

    class Meta:
        ordering = ['fecha', 'equipo_local', 'equipo_visitante']

class Jornada (models.Model):
    id_jornada = models.AutoField(primary_key=True)
    numero = models.IntegerField(unique=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['numero']