import unittest

from run import create_app

class FileManagerTestCase(unittest.TestCase):
    """Class for file manager module test cases."""
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app.app_context.push()

    # def getLoggedInUser(self):
    #     re = self.client().post('/', json={'username': 'mhird23', 
    #                                             'password': 'Passin123'})
    #     json_data = re.get_json()
    #     self.assertEqual(re.status_code, 201)

    # def testFileRead(self):
    #     re = self.client().post('/files', )

    def tearDown(self):
        self.app_context.pop()