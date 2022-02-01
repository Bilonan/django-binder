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
		# # Alt syntax
		# response = self.client.get('/caretaker/', data={'order_by': 'name', '.last_seen:range': '2017-03-23T10:00:00+0100,2017-03-25T00:00:00+0100'})

		# result = jsonloads(response.content)
		# self.assertEqual(2, len(result['data']))
		# self.assertEqual('Peter', result['data'][0]['name'])
		# self.assertEqual('Stefan', result['data'][1]['name'])


	# def test_text_filter_gte_match(self):
	# 	response = self.client.get('/caretaker/', data={'.last_seen:gte': '2017-03-23T11:26:14Z', 'order_by': 'last_seen'})

	# 	self.assertEqual(response.status_code, 200)

	# 	result = jsonloads(response.content)
	# 	self.assertEqual(2, len(result['data']))
	# 	self.assertEqual('Stefan', result['data'][0]['name'])
	# 	self.assertEqual('Peter', result['data'][1]['name'])

	# 	response = self.client.get('/caretaker/', data={'.last_seen:gte': '2017-03-23T12:00:00Z', 'order_by': 'last_seen'})

	# 	self.assertEqual(response.status_code, 200)

	# 	result = jsonloads(response.content)
	# 	self.assertEqual(1, len(result['data']))
	# 	self.assertEqual('Peter', result['data'][0]['name'])

	# 	response = self.client.get('/caretaker/', data={'.last_seen:gte': '2017-03-25T00:00:00Z'})

	# 	self.assertEqual(response.status_code, 200)

	# 	result = jsonloads(response.content)
	# 	self.assertEqual(0, len(result['data']))


	# def test_text_filter_gt_match(self):
	# 	# One second before earliest "last seen"
	# 	response = self.client.get('/caretaker/', data={'.last_seen:gt': '2017-03-23T11:26:13Z', 'order_by': 'last_seen'})

	# 	self.assertEqual(response.status_code, 200)

	# 	result = jsonloads(response.content)
	# 	self.assertEqual(2, len(result['data']))
	# 	self.assertEqual('Stefan', result['data'][0]['name'])
	# 	self.assertEqual('Peter', result['data'][1]['name'])

	# 	# One second later (exactly _on_ earliest "last seen")
	# 	response = self.client.get('/caretaker/', data={'.last_seen:gt': '2017-03-23T11:26:14Z', 'order_by': 'last_seen'})

	# 	self.assertEqual(response.status_code, 200)

	# 	result = jsonloads(response.content)
	# 	self.assertEqual(1, len(result['data']))
	# 	self.assertEqual('Peter', result['data'][0]['name'])

	# 	response = self.client.get('/caretaker/', data={'.last_seen:gt': '2017-03-25T00:00:00Z'})

	# 	self.assertEqual(response.status_code, 200)

	# 	result = jsonloads(response.content)
	# 	self.assertEqual(0, len(result['data']))


	# def test_text_filter_syntax_variations(self):
	# 	# Precise milliseconds
	# 	response = self.client.get('/caretaker/', data={'.last_seen:gt': '2017-03-23T11:26:13.9999Z', 'order_by': 'last_seen'})
	# 	self.assertEqual(response.status_code, 200)

	# 	result = jsonloads(response.content)
	# 	self.assertEqual(2, len(result['data']))

	# 	# Implicitly we add T23:59:59Z here to make this correct.
	# 	response = self.client.get('/caretaker/', data={'.last_seen:gt': '2017-03-23', 'order_by': 'last_seen'})
	# 	self.assertEqual(response.status_code, 200)

	# 	result = jsonloads(response.content)
	# 	self.assertEqual(1, len(result['data']))

	# 	# Same as above, but to the range start we add T00:00:00Z
	# 	response = self.client.get('/caretaker/', data={'.last_seen:range': '2017-03-23,2017-03-23', 'order_by': 'last_seen'})
	# 	self.assertEqual(response.status_code, 200)

	# 	result = jsonloads(response.content)
	# 	self.assertEqual(1, len(result['data']))

	# 	# Just a sanity check
	# 	response = self.client.get('/caretaker/', data={'.last_seen:range': '2017-03-23,2017-03-24', 'order_by': 'last_seen'})
	# 	self.assertEqual(response.status_code, 200)

	# 	result = jsonloads(response.content)
	# 	self.assertEqual(2, len(result['data']))

	# 	# You can't mix and match date and text syntax
	# 	response = self.client.get('/caretaker/', data={'.last_seen:range': '2017-03-23T00:00:00Z,2017-03-24', 'order_by': 'last_seen'})
	# 	self.assertEqual(response.status_code, 418)

	# def test_text_filter_syntax_variations_with_chained_qualifiers(self):
	# 	# Implicitly we add T23:59:59Z here to make this correct.
	# 	response = self.client.get(
	# 		'/caretaker/', data={'.last_seen:date:gt': '2017-03-23T23:59:59Z', 'order_by': 'last_seen'})
	# 	self.assertEqual(response.status_code, 200)

	# 	result = jsonloads(response.content)
	# 	self.assertEqual(1, len(result['data']))

	# 	# Same as above, but to the range start we add T00:00:00Z
	# 	response = self.client.get(
	# 		'/caretaker/', data={'.last_seen:date:range': '2017-03-23T23:59:59Z,2017-03-23T23:59:59Z', 'order_by': 'last_seen'})
	# 	self.assertEqual(response.status_code, 200)

	# 	result = jsonloads(response.content)
	# 	self.assertEqual(1, len(result['data']))

	# 	# Just a sanity check
	# 	response = self.client.get('/caretaker/', data={'.last_seen:date:range': '2017-03-23T23:59:59Z,2017-03-24T23:59:59Z', 'order_by': 'last_seen'})
	# 	self.assertEqual(response.status_code, 200)

	# 	result = jsonloads(response.content)
	# 	self.assertEqual(2, len(result['data']))
  
	# def test_text_filter_syntax_errors_cause_error_response(self):
	# 	response = self.client.get('/caretaker/', data={'.last_seen': '1838-05'})
	# 	self.assertEqual(response.status_code, 418)

	# 	response = self.client.get('/caretaker/', data={'.last_seen': '1838-05-01-02'})
	# 	self.assertEqual(response.status_code, 418)

	# 	# Incomplete timestamp
	# 	response = self.client.get('/caretaker/', data={'.last_seen': '1838-05-01T02:10'})
	# 	self.assertEqual(response.status_code, 418)

	# 	# Missing +/- (or too many seconds)
	# 	response = self.client.get('/caretaker/', data={'.last_seen': '1838-05-01T02:10:0220'})
	# 	self.assertEqual(response.status_code, 418)

	# def test_text_isnull(self):
	# 	# Due to corona, I forgot when I last saw bob
	# 	Caretaker(name='Bob', last_seen=None).save()
	# 	response = self.client.get('/caretaker/', data={'.last_seen:isnull': 'True'})
	# 	result = jsonloads(response.content)

	# 	# We only get bob back with no data
	# 	self.assertEqual(1, len(result['data']))
	# 	self.assertEqual('Bob', result['data'][0]['name'])

	# def test_text__isnull_false(self):
	# 	# Due to corona, I forgot when I last saw bob
	# 	Caretaker(name='Bob', last_seen=None).save()

	# 	for false_value in ['0', 'false', 'False']:

	# 		response = self.client.get('/caretaker/', data={'.last_seen:isnull': false_value})
	# 		result = jsonloads(response.content)

	# 		# We only get bob back with no data
	# 		self.assertEqual(2, len(result['data']))
	# 		self.assertNotEqual('Bob', result['data'][0]['name'])
	# 		self.assertNotEqual('Bob', result['data'][1]['name'])
