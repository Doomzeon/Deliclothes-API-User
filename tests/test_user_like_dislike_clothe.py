from pathlib import Path
import os
import sys
sys.path.insert(0, str(os.path.dirname(os.getcwd())))
from bin.server import app
import unittest
import json

class ApiTestUsernameActions(unittest.TestCase):
    
    
    def test_like_clothe(self):
        tester = app.test_client(self)
        test_data = {
            "payload":{
                    "id_clothe":'86009030',
                    "id_user":1,
                    "brand":'Zara'
                }
            
        }
        response = tester.post('/api_v1/user/like_clothe',data= json.dumps(test_data), content_type='application/json')
        print(response.get_json())
        self.assertEqual(response.status_code, 200)

    
    def test_select_liked_clothes(self):
        tester = app.test_client(self)
        response = tester.get('/api_v1/user/1/liked_clothes')
        print(response.get_json())
        self.assertEqual(response.status_code, 200)
    
    
    def test_select_dislike_clothe(self):
        tester = app.test_client(self)
        response = tester.delete('/api_v1/user/dislike_clothe/86009030/1')
        print(response.get_json())
        self.assertEqual(response.status_code, 200)
        
        




if __name__ == '__main__':
    unittest.main()



