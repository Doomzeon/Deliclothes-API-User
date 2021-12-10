from pathlib import Path
import os
import sys
sys.path.insert(0, str(os.path.dirname(os.getcwd())))
from bin.server import app
import unittest
import json

class ApiTestUsernameActions(unittest.TestCase):
    
    
    def test_process_of_bying_clothes(self):
        tester = app.test_client(self)
        test_data = {
            "payload":{
                "customer_id":"cus_JCkUDYqIyouRy0",
                "email_customer":'osetskiivadim1@gmail.com',
                "amount":"100",
                "id_user":17,
                "hour_delivery":"12:30",
                "day_delivery":"02/01/2021",
                "street_delivery":'via test',
                "city_id_delivery":0,
                "credit_card_id":5,
                "clothes_dict":[{
                    "test":"test"
                    }],
                "card_id_stripe":'pm_1IaKzIHRpyaXtqnWiAHX4YCz',
                }
            
        }
        response = tester.post('/api_v1/user/procced_order',data= json.dumps(test_data), content_type='application/json')
        print(response.get_json())
        self.assertEqual(response.status_code, 200)





if __name__ == '__main__':
    unittest.main()
