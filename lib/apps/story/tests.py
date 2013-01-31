from django.core import exceptions
from django.test import TestCase
from models import Genre

class GenreTestCase(TestCase):
	""" Just learning Django unit testing here.. """
	def setUp(self):
		pass

	def test_should_save_valid_genre(self):
		genre = Genre(name='TestGenre', description='This is a description')
		genre.save()
		all_genres = Genre.objects.all()
		self.assertEqual(len(all_genres), 1)

	def test_should_not_save_invalid_genre(self):
		title = ("HA" * 128) + "!" # 257 chars
		genre = Genre(name=title, description='')
		self.assertRaises(exceptions.ValidationError, genre.full_clean)

	def tearDown(self):
		pass

		
