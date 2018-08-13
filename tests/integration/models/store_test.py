from models.item import ItemModel
from models.store import StoreModel

from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel("test store")

        self.assertListEqual(
            store.items.all(),
            [],
            "The store list is not empty: {} item{}!".format(
                len(store.items.all()), 's' if len(store.items.all()) > 1 else ''
            )
        )

    def test_crud(self):
        with self.app_context():
            store = StoreModel("test store")

            self.assertIsNone(StoreModel.find_by_name("test store"))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name("test store"))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name("test store"))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel("test store")
            item = ItemModel("test_item", 19.99, 1)

            store.save_to_db()          # needs to be before saving the item
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, "test_item")

    def test_store_json(self):
        store = StoreModel("test store")
        expected = {
            "id": None,
            "name": "test store",
            "items": [],
        }

        self.assertDictEqual(store.json(), expected)


    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel("test store")
            item = ItemModel("test_item", 19.77, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {
                "id": 1,
                "name": "test store",
                "items": [{"name": "test_item", "price": 19.77}],
            }

            self.assertDictEqual(store.json(), expected)












