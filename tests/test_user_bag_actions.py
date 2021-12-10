from pathlib import Path
import os
import sys
sys.path.insert(0, str(os.path.dirname(os.getcwd())))
from bin.server import app
import unittest
import json

class ApiTestUsernameActions(unittest.TestCase):
        
    """def test_add_clothe_to_the_bag(self):
        tester = app.test_client(self)
        test_data = {
            "payload":{
                    "id_clothe":'86009030',
                    "id_user":1,
                    "brand":'Zara',
                    "size":'S',
                    "id_size":'06840065407',
                    'quantity':2
                }
            
        }
        response = tester.post('/api_v1/user/add_clothe_to_the_bag',data= json.dumps(test_data), content_type='application/json')
        print(response.get_json())
        self.assertEqual(response.status_code, 200)"""
        
    """def test_selectd_clothe_from_the_bag(self):
        tester = app.test_client(self)
        response = tester.get('/api_v1/user/1/clothes_in_the_bag')
        print(response.get_json())
        self.assertEqual(response.status_code, 200)"""
    
        
        
    def test_remove_clothe_from_the_bag(self):
        tester = app.test_client(self)
        response = tester.delete('/api_v1/user/remove_clothe_from_the_bag/86009030/1')
        print(response.get_json())
        self.assertEqual(response.status_code, 202)


if __name__ == '__main__':
    unittest.main()