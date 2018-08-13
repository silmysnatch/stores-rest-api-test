from models.item import ItemModel
from models.user import UserModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json

class ItemTest(BaseTest):

    access_token = ""

    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel("test_user", "1234").save_to_db()
                auth_request = client.post(
                    "/auth",
                    data=json.dumps({"username": "test_user", "password": "1234"}),
                    headers={"Content-Type": "application/json"},
                )

                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = "JWT " + auth_token


    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get("/item/test")
                self.assertEqual(response.status_code, 401)
                self.assertDictEqual(
                    {"message": "Could not authorize. Did you include a valid Authorization Header"},
                    json.loads(response.data),
                )


    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():

                response = client.get("/item/test", headers={"Authorization": self.access_token})
                self.assertEqual(404, response.status_code)

    def test_pass_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test", 99.65, 1).save_to_db()
                response = client.get("/item/test", headers={"Authorization": self.access_token})
                self.assertEqual(200, response.status_code)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test", 99.65, 1).save_to_db()
                self.assertIsNotNone(ItemModel.find_by_name("test"))
                response = client.delete("/item/test", headers={"Authorization": self.access_token})
                self.assertEqual(200, response.status_code)
                self.assertIsNone(ItemModel.find_by_name("test"))
                self.assertDictEqual({"message": "Item deleted"}, json.loads(response.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()

                response = client.post("/item/test", data={"price": 32.11, "store_id": 1}, headers={"Authorization": self.access_token})
                self.assertEqual(201, response.status_code)
                self.assertIsNotNone(ItemModel.find_by_name("test"))
                self.assertDictEqual(
                    {
                        "name": "test",
                        "price": 32.11,
                    },
                    json.loads(response.data)
                )


    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                ItemModel("test", 25.00, 1).save_to_db()
                self.assertIsNotNone(ItemModel.find_by_name("test"))
                response = client.post("/item/test", data={"price": 32.11, "store_id": 1},
                                       headers={"Authorization": self.access_token})
                self.assertEqual(400, response.status_code)
                self.assertDictEqual(
                    {
                        "message": "An item with name 'test' already exists."
                    },
                    json.loads(response.data)
                )

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                self.assertIsNone(ItemModel.find_by_name("test"))

                response = client.put("/item/test",
                                      data={"price": 30.00, "store_id":1},
                                      headers={"Authorization": self.access_token}
                                      )
                self.assertEqual(200, response.status_code)
                self.assertDictEqual(
                    {"name": "test", "price": 30.00},
                    json.loads(response.data)
                )

    def test_put_item_update(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                ItemModel("test", 54.11, 1).save_to_db()
                self.assertEqual(54.11, ItemModel.find_by_name("test").price)

                response = client.put("/item/test",
                                      data={"price": 30.00, "store_id":1},
                                      headers={"Authorization": self.access_token}
                                      )
                self.assertEqual(200, response.status_code)
                self.assertDictEqual(
                    {"name": "test", "price": 30.00},
                    json.loads(response.data)
                )

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test store").save_to_db()
                ItemModel("test1", 45.00, 1).save_to_db()
                ItemModel("test2", 56.00, 1).save_to_db()
                response = client.get("/items")
                self.assertEqual(200, response.status_code)
                self.assertDictEqual(
                    {
                        "items": [
                            {"name": "test1", "price": 45.00},
                            {"name": "test2", "price": 56.00}
                        ]
                    },
                    json.loads(response.data)
                )
