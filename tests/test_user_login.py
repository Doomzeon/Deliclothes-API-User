from pathlib import Path
import os
import sys
sys.path.insert(0, str(os.path.dirname(os.getcwd())))
from bin.server import app
import unittest
import json

class ApiTestUsernameActions(unittest.TestCase):
    
    
    def test_login_user(self):
        tester = app.test_client(self)
        test_data = {
            "payload":{
                "email":"osetskiivadim1@gmail.com",
                "password":'test'
                }
            
        }
        response = tester.post('/api_v1/user/login',data= json.dumps(test_data), content_type='application/json')
        print(response.get_json())
        self.assertEqual(response.status_code, 200)





if __name__ == '__main__':
    unittest.main()



