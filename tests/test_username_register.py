from pathlib import Path
import os
import sys
sys.path.insert(0, str(os.path.dirname(os.getcwd())))
from bin.server import app
import unittest
import json

class ApiTestUsernameActions(unittest.TestCase):
    
    
    def test_register_new_user(self):
        tester = app.test_client(self)
        test_data = {
            "payload":{
                "email":"osetskiivadim1@gmail.com",
                "password":'test',
                "name":'test',
                "surname":'test',
                "residence": 'via Test',
                "id_city":0,
                "city":'Milan',
                "country":'IT',
                "phone_number":334567543,
                "country_code":"+39",
                "language":'it',
                "zip_code":20032,
                "credit_card":{
                    "title":'Test 2 credit card',
                    "owner":'Test Test',
                    "card_number":"4242424242424242",
                    "expiration_month":3,
                    "expiration_year":2022,
                    "cvc":314,
                    "card_type":"card"
                }
            }
        }
        response = tester.post('/api_v1/user/register',data= json.dumps(test_data),content_type='application/json')
        print(response.get_json())
        self.assertEqual(response.status_code, 201)
    
    





if __name__ == '__main__':
    unittest.main()



