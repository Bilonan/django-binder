from binder.views import ModelView

from ..models import Zoo

# From the api docs
class ZooView(ModelView):
	m2m_fields = ['contacts', 'zoo_employees', 'most_popular_animals']
	model = Zoo
	file_fields = ['floor_plan']
	shown_properties = ['animal_count']

	def get_rooms_for_user(user):
		return [
			{
				'zoo': 'all',
			},
		]
