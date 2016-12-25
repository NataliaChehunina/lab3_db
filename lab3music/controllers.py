from .views import View
from django.http import HttpResponse, HttpResponseRedirect
from .models import *

class AbstractController:

	table = ''
	model = ''

	def get(self, request):
		return View(self.table + '.html', request, self.model.objects.all()).renderPage()

	def add(self, request):
		if self.model(self.table).add(request.GET):
			return HttpResponse(1)
		return HttpResponse(0)

	def delete(self, request):
		self.model.objects.filter(id = request.GET['id']).delete()
		return HttpResponseRedirect('/' + self.table + '/get')

class IndexController (AbstractController):

	def __init__(self):
		self.table = 'index'

	def get(self, request):
		return View(self.table + '.html', request, []).renderPage()

	def add(self, request):
		with open('lab3music/static/db.json') as dataFile:
			data = json.load(dataFile)
			for self.table in data:
				self.model = self.table
				for row in data[self.table]:
					super().add(row)
		return True

class ArtistsController (AbstractController):

	def __init__(self):
		self.table = 'artists'
		self.model = Artists

	def update(self, request):
		self.model.objects.filter(id = request.GET['id']).update(name = request.GET['name'], country = request.GET['country'])
		return HttpResponse(1)

class TracksController (AbstractController):

	def __init__(self):
		self.table = 'tracks'
		self.model = Tracks

class StudiosController (AbstractController):

	def __init__(self):
		self.table = 'studios'
		self.model = Studios

	def update(self, request):
		self.model.objects.filter(id = request.GET['id']).update(name = request.GET['name'])
		return HttpResponse(1)

class AlbumsController (AbstractController):

	def __init__(self):
		self.table = 'albums'
		self.model = Albums