import json

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test_store')

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name("test_store"))
                self.assertDictEqual({
                    "id": 1,
                    "name": "test_store",
                    "items": []},
                    json.loads(response.data)
                )

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store')
                response = client.post('/store/test_store')

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({
                    "message": "A store with name 'test_store' already exists."},
                    json.loads(response.data),
                )

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store')
                self.assertIsNotNone(StoreModel.find_by_name("test_store"))
                response = client.delete("/store/test_store")
                self.assertIsNone(StoreModel.find_by_name("test_store"))
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({
                    "message": "Store deleted"},
                    json.loads(response.data)
                )

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                # client.post('/store/test_store')
                StoreModel("test_store").save_to_db()
                self.assertIsNotNone(StoreModel.find_by_name("test_store"))
                response = client.get('/store/test_store')
                expected = {'id': 1, 'name': 'test_store', 'items': []}
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), expected)

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                self.assertIsNone(StoreModel.find_by_name("test_store"))
                response = client.get('/store/test_store')
                expected = {"message": "Store not found"}
                self.assertEqual(response.status_code, 404)
                self.assertDictEqual(json.loads(response.data), expected)

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                # client.post('/store/test_store')
                StoreModel("test_store").save_to_db()
                self.assertIsNotNone(StoreModel.find_by_name("test_store"))
                item = ItemModel("test item", 99.99, 1)
                item.save_to_db()
                response = client.get('/store/test_store')
                expected = {'id': 1, 'name': 'test_store', 'items': [{"name": "test item",
                                                             "price": 99.99
                                                             }]}
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), expected)


    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                # client.post('/store/test_store1')
                # client.post('/store/test_store2')
                # client.post('/store/test_store3')
                StoreModel("test_store1").save_to_db()
                StoreModel("test_store2").save_to_db()
                StoreModel("test_store3").save_to_db()
                response = client.get('/stores')
                expected = {
                    "stores": [
                        {'id': 1, 'name': 'test_store1', 'items': []},
                        {'id': 2, 'name': 'test_store2', 'items': []},
                        {'id': 3, 'name': 'test_store3', 'items': []},
                    ],
                }
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), expected)


    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store1')
                client.post('/store/test_store2')
                client.post('/store/test_store3')
                item2 = ItemModel("test item2", 37.43, 2)
                item2.save_to_db()
                response = client.get('/stores')
                expected = {
                    "stores": [
                        {'id': 1, 'name': 'test_store1', 'items': []},
                        {'id': 2, 'name': 'test_store2', 'items': [{"name": "test item2", "price": 37.43}]},
                        {'id': 3, 'name': 'test_store3', 'items': []},
                    ],
                }
                self.assertDictEqual(json.loads(response.data), expected)
