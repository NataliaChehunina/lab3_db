import json
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class Artists (models.Model):

	id = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 100)
	country = models.CharField(max_length = 100)

	class Meta:
		db_table = 'artists'

	def add(self, data):
		Artists(name = data['name'], country = data['country']).save()
		return Artists.objects.latest('id')
#
class Studios (models.Model):

	id = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 100)

	def add(self, data):
		Studios(name = data['name']).save()
		return Artists.objects.latest('id')
	
	class Meta:
		db_table = 'studios'
#
class Albums (models.Model):

	id = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 100)
	year = models.IntegerField()
	artist = models.ForeignKey(Artists, on_delete = models.CASCADE)
	style = models.CharField(max_length = 100)
	studio = models.ForeignKey(Studios, on_delete = models.CASCADE)

	def add(self, data):
		try:
			artist = Artists.objects.get(name = data['artist'])
			studio = Studios.objects.get(name = data['studio'])
			Albums(name = data['album'], year = data['year'], artist = artist, style = data['style'], studio = studio).save()
			return Albums.objects.latest('id')
		except ObjectDoesNotExist:
			return False
	
	class Meta:
		db_table = 'albums'
#
class Tracks (models.Model):

	id = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 100)
	date_record = models.CharField(max_length = 100)
	duration = models.CharField(max_length = 100)
	album = models.ForeignKey(Albums, on_delete = models.CASCADE)

	def add(self, data):
		try:
			album = Albums.objects.get(name = data['album'])
			Tracks(name = data['track'], album = album, date_record = data['date_record'], duration = data['duration']).save()
			return Tracks.objects.latest('id')
		except ObjectDoesNotExist:
			return False
	
	class Meta:
		db_table = 'tracks'