import json
from os import urandom
from PIL import Image
from tempfile import NamedTemporaryFile
from django.test import TestCase, Client

from binder.json import jsonloads
from django.core.files import File
from django.contrib.auth.models import User

from .testapp.models import Animal, Zoo

def image(width, height):
	return Image.frombytes('RGB', (width, height), urandom(width * height * 3))

def temp_imagefile(width, height, format):
	i = image(width, height)
	f = NamedTemporaryFile(suffix='.jpg')
	i.save(f, format)
	f.seek(0)
	return f


class FileUploadTest(TestCase):
	def setUp(self):
		super().setUp()
		u = User(username='testuser', is_active=True, is_superuser=True)
		u.set_password('test')
		u.save()
		self.client = Client()
		r = self.client.login(username='testuser', password='test')
		self.assertTrue(r)

	# Clean up uploaded files
	def tearDown(self):
		Zoo.objects.all().delete()


	def test_get_model_with_file(self):
		emmen = Zoo(name='Wildlands Adventure Zoo Emmen')

		file = temp_imagefile(100, 200, 'jpeg')
		emmen.floor_plan.save('plan.jpg', File(file), save=False)
		emmen.save()

		response = self.client.get('/zoo/%d/' % emmen.id)
		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		self.assertEqual(emmen.id, result['data']['id'])
		self.assertEqual(emmen.name, result['data']['name'], 'Wildlands Adventure Zoo Emmen')
		self.assertEqual('/zoo/%d/floor_plan/' % emmen.id, result['data']['floor_plan'])


	# This is a basic regression test for a bug due to the router
	# singleton refactor, GET would crash if the model simply
	# _contained_ a file attribute.
	def test_get_related_model_with_file(self):
		emmen = Zoo(name='Wildlands Adventure Zoo Emmen')

		file = temp_imagefile(100, 200, 'jpeg')
		emmen.floor_plan.save('plan.jpg', File(file), save=False)
		emmen.save()

		donald = Animal(name='Donald Duck', zoo=emmen)
		donald.save()

		response = self.client.get('/animal/%d/' % donald.id, data={'with': 'zoo'})
		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		self.assertEqual(donald.id, result['data']['id'])
		self.assertEqual({'zoo': 'zoo'}, result['with_mapping'])

		zoo = result['with']['zoo'][0]
		self.assertEqual(emmen.id, zoo['id'])
		self.assertEqual(emmen.name, zoo['name'], 'Wildlands Adventure Zoo Emmen')
		self.assertEqual('/zoo/%d/floor_plan/' % emmen.id, zoo['floor_plan'])
