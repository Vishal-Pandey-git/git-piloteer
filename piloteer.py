from proj.inventory import MobileInventory, InsufficientException
import sys
import os

sys.path.append(os.getcwd())
import pytest


class TestingInventoryCreation:
    def test_creating_empty_inventory(self):
        x = MobileInventory()
        assert x.balance_inventory == {}

    def test_creating_specified_inventory(self):
        x = MobileInventory({
            'iPhone Model X': 100,
            'Xiaomi Model Y': 1000,
            'Nokia Model Z': 25
        })
        assert {
            'iPhone Model X': 100,
            'Xiaomi Model Y': 1000,
            'Nokia Model Z': 25
        } == x.balance_inventory

    def test_creating_inventory_with_list(self):
        with pytest.raises(TypeError) as excinfo:
            MobileInventory(
                ['iPhone Model X', 'Xiaomi Model Y', 'Nokia Model Z'])
        assert "Input inventory must be a dictionary" == str(excinfo.value)

    def test_creating_inventory_with_numeric_keys(self):
        with pytest.raises(ValueError) as excinfo:
            MobileInventory({
                1: 'iPhone Model X',
                2: 'Xiaomi Model Y',
                3: 'Nokia Model Z'
            })
        assert "Mobile model name must be a string" == str(excinfo.value)

    def test_creating_inventory_with_nonnumeric_values(self):
        with pytest.raises(ValueError) as excinfo:
            MobileInventory({
                'iPhone Model X': '100',
                'Xiaomi Model Y': '1000',
                'Nokia Model Z': '25'
            })
        assert "No. of mobiles must be a positive integer" == str(
            excinfo.value)

    def test_creating_inventory_with_negative_value(self):
        with pytest.raises(ValueError) as excinfo:
            MobileInventory({
                'iPhone Model X': -45,
                'Xiaomi Model Y': 200,
                'Nokia Model Z': 25
            })
        assert "No. of mobiles must be a positive integer" == str(
            excinfo.value)


class TestInventoryAddStock:
    @classmethod
    def setup_class(cls):
        cls.inventory = MobileInventory({
            'iPhone Model X': 100,
            'Xiaomi Model Y': 1000,
            'Nokia Model Z': 25
        })

    def test_add_new_stock_as_dict(self):
        self.inventory.add_stock({
            "iPhone Model X": 50,
            "Xiaomi Model Y": 2000,
            "Nokia Model A": 10
        })
        assert {
            "iPhone Model X": 150,
            "Xiaomi Model Y": 3000,
            "Nokia Model Z": 25,
            "Nokia Model A": 10
        } == self.inventory.balance_inventory

    def test_add_new_stock_as_list(self):
        with pytest.raises(TypeError) as excinfo:
            self.inventory.add_stock(
                ['iPhone Model X', 'Xiaomi Model Y', 'Nokia Model Z'])
        assert "Input stock must be a dictionary" == str(excinfo.value)

    def test_add_new_stock_with_numeric_keys(self):
        with pytest.raises(ValueError) as excinfo:
            self.inventory.add_stock({
                1: 'iPhone Model A',
                2: 'Xiaomi Model B',
                3: 'Nokia Model C'
            })
        assert "Mobile model name must be a string" == str(excinfo.value)

    def test_add_new_stock_with_nonnumeric_values(self):
        with pytest.raises(ValueError) as excinfo:
            self.inventory.add_stock({
                "iPhone Model A": "50",
                "Xiaomi Model B": "2000",
                "Nokia Model C": "25"
            })
        assert "No. of mobiles must be a positive integer" == str(
            excinfo.value)

    def test_add_new_stock_with_float_values(self):
        with pytest.raises(ValueError) as excinfo:
            self.inventory.add_stock({
                'iPhone Model A': 50.5,
                'Xiaomi Model B': 2000.3,
                'Nokia Model C': 25
            })
        assert "No. of mobiles must be a positive integer" == str(
            excinfo.value)


class TestInventorySellStock:
    @classmethod
    def setup_class(cls):
        cls.inventory = MobileInventory({
            'iPhone Model A': 50,
            'Xiaomi Model B': 2000,
            'Nokia Model C': 10,
            'Sony Model D': 1
        })

    def test_sell_stock_as_dict(self):
        self.inventory.sell_stock({
            'iPhone Model A': 2,
            'Xiaomi Model B': 20,
            'Sony Model D': 1
        })
        assert self.inventory.balance_inventory == {
            'iPhone Model A': 48,
            'Xiaomi Model B': 1980,
            'Nokia Model C': 10,
            'Sony Model D': 0
        }

    def test_sell_stock_as_list(self):
        with pytest.raises(TypeError) as excinfo:
            self.inventory.sell_stock(
                ["iPhone Model A", "Xiaomi Model B", "Nokia Model C"])
        assert "Requested stock must be a dictionary" == str(excinfo.value)

    def test_sell_stock_with_numeric_keys(self):
        with pytest.raises(ValueError) as excinfo:
            self.inventory.sell_stock(
                MobileInventory({
                    1: 'iPhone Model A',
                    2: 'Xiaomi Model B',
                    3: 'Nokia Model C'
                }))
        assert "Mobile model name must be a string" == str(excinfo.value)

    def test_sell_stock_with_nonnumeric_values(self):
        with pytest.raises(ValueError) as excinfo:
            self.inventory.sell_stock(
                MobileInventory({
                    'iPhone Model A': '2',
                    'Xiaomi Model B': '3',
                    'Nokia Model C': '4'
                }))
        assert "No. of mobiles must be a positive integer" == str(
            excinfo.value)

    def test_sell_stock_with_float_values(self):
        with pytest.raises(ValueError) as excinfo:
            self.inventory.sell_stock(
                MobileInventory({
                    'iPhone Model A': 2.5,
                    'Xiaomi Model B': 3.1,
                    'Nokia Model C': 4
                }))
        assert "No. of mobiles must be a positive integer" == str(
            excinfo.value)

    def test_sell_stock_of_nonexisting_model(self):
        with pytest.raises(InsufficientException) as excinfo:
            self.inventory.sell_stock({
                'iPhone Model B': 2,
                'Xiaomi Model B': 5
            })
        assert "No Stock. New Model Request" == str(excinfo.value)

    def test_sell_stock_of_insufficient_stock(self):
        with pytest.raises(InsufficientException) as excinfo:
            self.inventory.sell_stock({
                'iPhone Model A': 2,
                'Xiaomi Model B': 5,
                'Nokia Model C': 15
            })
        assert "Insufficient Stock" == str(excinfo.value)