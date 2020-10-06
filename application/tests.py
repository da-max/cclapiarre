import json

from graphene_django.utils.testing import GraphQLTestCase


class ApplicationTestCase(GraphQLTestCase):
    def test_all_applications_query(self):
        response = self.query(
            '''
      query {
        allApplications {
          id,
          name,
          table
        }
      }
      ''')
        self.assertEqual(response.status_code, 200)
