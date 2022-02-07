from django.test import TestCase, Client
from binder.json import jsonloads
from django.contrib.auth.models import User
from django.contrib.postgres.operations import UnaccentExtension

from ..testapp.models import Caretaker

class TextFiltersTest(TestCase):
	def setUp(self):
		super().setUp()
		UnaccentExtension()
		u = User(username='testuser', is_active=True, is_superuser=True)
		u.set_password('test')
		u.save()
		self.client = Client()
		r = self.client.login(username='testuser', password='test')
		self.assertTrue(r)

		Caretaker(name='Peter').save()
		Caretaker(name='Stefan').save()


	def test_text_filter_exact_match(self):
		response = self.client.get('/caretaker/', data={'.name': 'Stefan'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		self.assertEqual(1, len(result['data']))
		self.assertEqual('Stefan', result['data'][0]['name'])

		response = self.client.get('/caretaker/', data={'.name': 'Stefa'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		self.assertEqual(0, len(result['data']))


	# [TODO] unaccent needs to be installed as an extension on postgres to make it work
	# def test_text_filter_unaccent_chained_qualifier_match(self):
	# 	response = self.client.get('/caretaker/', data={'.name:unaccent': 'Śtefan'})

	# 	self.assertEqual(response.status_code, 200)

	# 	result = jsonloads(response.content)
	# 	self.assertEqual(0, len(result['data']))

	def test_text_filter_iexact(self):
		response = self.client.get('/caretaker/', data={'.name:iexact': 'stefan'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		print(result)
		self.assertEqual(1, len(result['data']))
		self.assertEqual('Stefan', result['data'][0]['name'])

		response = self.client.get('/caretaker/', data={'.name:iexact': 'sTEfaN'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		print(result)
		self.assertEqual(1, len(result['data']))
		self.assertEqual('Stefan', result['data'][0]['name'])

	def test_text_filter_contains(self):
		response = self.client.get('/caretaker/', data={'.name:contains': 'stef'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		print(result)
		self.assertEqual(0, len(result['data']))
  
		response = self.client.get('/caretaker/', data={'.name:contains': 'Stef'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		print(result)
		self.assertEqual(1, len(result['data']))
		self.assertEqual('Stefan', result['data'][0]['name'])

		response = self.client.get('/caretaker/', data={'.name:contains': 'e'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		print(result)
		self.assertEqual(2, len(result['data']))

	def test_text_filter_icontains(self):
		response = self.client.get('/caretaker/', data={'.name:icontains': 'stefi'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		print(result)
		self.assertEqual(0, len(result['data']))

		response = self.client.get('/caretaker/', data={'.name:icontains': 'sTEf'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		print(result)
		self.assertEqual(1, len(result['data']))
		self.assertEqual('Stefan', result['data'][0]['name'])

		response = self.client.get('/caretaker/', data={'.name:icontains': 'E'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		print(result)
		self.assertEqual(2, len(result['data']))

	def test_text_filter_startswith(self):
		response = self.client.get('/caretaker/', data={'.name:startswith': 'tef'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		print(result)
		self.assertEqual(0, len(result['data']))

		response = self.client.get('/caretaker/', data={'.name:startswith': 'Stef'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		print(result)
		self.assertEqual(1, len(result['data']))
		self.assertEqual('Stefan', result['data'][0]['name'])

		response = self.client.get('/caretaker/', data={'.name:startswith': 'ste'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		print(result)
		self.assertEqual(0, len(result['data']))

	def test_text_filter_istartswith(self):
		response = self.client.get('/caretaker/', data={'.name:istartswith': 'tef'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		print(result)
		self.assertEqual(0, len(result['data']))

		response = self.client.get('/caretaker/', data={'.name:istartswith': 'stef'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		print(result)
		self.assertEqual(1, len(result['data']))
		self.assertEqual('Stefan', result['data'][0]['name'])

		response = self.client.get('/caretaker/', data={'.name:istartswith': 'sTEF'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		print(result)
		self.assertEqual(1, len(result['data']))
		self.assertEqual('Stefan', result['data'][0]['name'])
  
	def test_text_filter_endswith(self):
		response = self.client.get('/caretaker/', data={'.name:endswith': 'efa'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		print(result)
		self.assertEqual(0, len(result['data']))

		response = self.client.get('/caretaker/', data={'.name:endswith': 'efan'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		print(result)
		self.assertEqual(1, len(result['data']))
		self.assertEqual('Stefan', result['data'][0]['name'])

		response = self.client.get('/caretaker/', data={'.name:endswith': 'efaN'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		print(result)
		self.assertEqual(0, len(result['data']))

	def test_text_filter_iendswith(self):
		response = self.client.get('/caretaker/', data={'.name:iendswith': 'efa'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		print(result)
		self.assertEqual(0, len(result['data']))

		response = self.client.get('/caretaker/', data={'.name:iendswith': 'EfAn'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		print(result)
		self.assertEqual(1, len(result['data']))
		self.assertEqual('Stefan', result['data'][0]['name'])

		response = self.client.get('/caretaker/', data={'.name:iendswith': 'efaN'})

		self.assertEqual(response.status_code, 200)

		result = jsonloads(response.content)
		print(result)
		self.assertEqual(1, len(result['data']))
		self.assertEqual('Stefan', result['data'][0]['name'])
	