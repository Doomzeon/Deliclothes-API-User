import flask_pymongo as pymongo


class DatabaseMD():

    def __init__(self):
        try:
            self.mongodb_client = pymongo.MongoClient(
                "mongodb+srv://admin:admin@couriers.vyr0z.mongodb.net/Couriers?retryWrites=true&w=majority")
            print(self.mongodb_client.db)
            self.db = self.mongodb_client.Couriers
        except Exception as e:
            raise(e)
        
    
    def select_orders_order_by_time_asc_and_group_by_couriers(self):
        try:
            list_couriers_orders_times =  self.db.courier.aggregate([
                {
                    '$unwind': {
                        'path': '$orders'
                    }
                }, {
                    '$sort': {
                        'id': 1, 
                        'orders.time_start': 1
                    }
                }, {
                    '$group': {
                        '_id': {
                            'courier_id': '$id'
                        }, 
                        'orders': {
                            '$push': '$orders'
                        }
                    }
                }
            ])
            return list_couriers_orders_times
        except Exception as e:
            print(e)