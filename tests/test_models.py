# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR
# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Product Model
"""

import os
import logging
import unittest
from decimal import Decimal

from service.models import Product, Category, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    # TEST CASES
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(
            name="Fedora",
            description="A red hat",
            price=12.50,
            available=True,
            category=Category.CLOTHS,
        )
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.category, Category.CLOTHS)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])

        product = ProductFactory()
        product.id = None
        product.create()

        self.assertIsNotNone(product.id)

        products = Product.all()
        self.assertEqual(len(products), 1)

        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        self.assertEqual(Decimal(new_product.price), product.price)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)

    def test_read_a_product(self):
        """It should Read a Product from the database"""
        product = ProductFactory()
        product.create()

        found_product = Product.find(product.id)

        self.assertIsNotNone(found_product)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.description, product.description)
        self.assertEqual(Decimal(found_product.price), product.price)
        self.assertEqual(found_product.available, product.available)
        self.assertEqual(found_product.category, product.category)

    def test_update_a_product(self):
        """It should Update a Product in the database"""
        product = ProductFactory()
        product.create()

        product.name = "Updated Product"
        product.description = "Updated description"
        product.price = Decimal("25.50")
        product.available = False
        product.category = Category.FOOD
        product.update()

        found_product = Product.find(product.id)

        self.assertEqual(found_product.name, "Updated Product")
        self.assertEqual(found_product.description, "Updated description")
        self.assertEqual(found_product.price, Decimal("25.50"))
        self.assertFalse(found_product.available)
        self.assertEqual(found_product.category, Category.FOOD)

    def test_delete_a_product(self):
        """It should Delete a Product from the database"""
        product = ProductFactory()
        product.create()

        product_id = product.id
        product.delete()

        found_product = Product.find(product_id)

        self.assertIsNone(found_product)

    def test_list_all_products(self):
        """It should List all Products in the database"""
        products = ProductFactory.create_batch(5)

        for product in products:
            product.id = None
            product.create()

        found_products = Product.all()

        self.assertEqual(len(found_products), 5)

    def test_find_by_name(self):
        """It should Find Products by name"""
        product1 = ProductFactory(name="Fedora")
        product1.create()

        product2 = ProductFactory(name="Fedora")
        product2.create()

        product3 = ProductFactory(name="Boots")
        product3.create()

        found_products = Product.find_by_name("Fedora")

        self.assertEqual(found_products.count(), 2)

        for product in found_products:
            self.assertEqual(product.name, "Fedora")

    def test_find_by_category(self):
        """It should Find Products by category"""
        product1 = ProductFactory(category=Category.CLOTHS)
        product1.create()

        product2 = ProductFactory(category=Category.CLOTHS)
        product2.create()

        product3 = ProductFactory(category=Category.FOOD)
        product3.create()

        found_products = Product.find_by_category(Category.CLOTHS)

        self.assertEqual(found_products.count(), 2)

        for product in found_products:
            self.assertEqual(product.category, Category.CLOTHS)

    def test_find_by_availability(self):
        """It should Find Products by availability"""
        product1 = ProductFactory(available=True)
        product1.create()

        product2 = ProductFactory(available=True)
        product2.create()

        product3 = ProductFactory(available=False)
        product3.create()

        found_products = Product.find_by_availability(True)

        self.assertEqual(found_products.count(), 2)

        for product in found_products:
            self.assertTrue(product.available)
