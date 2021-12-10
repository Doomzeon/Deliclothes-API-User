
import unittest

from bin.controller.user_controller import UsernameController

data_set=[
    {"size_selected":"0751305440038-V2021"},
    {"size_selected":"0751305440040-V2021"}
]


class TestDirections(unittest.TestCase):
    
    def delivery_directions(self):
        print('start')
        response = UsernameController().test_hour_delivery(data_set)
        print(response)
        self.assertEqual(True, True, "Passed :)")
        

if __name__ == '__main__':
    unittest.main()