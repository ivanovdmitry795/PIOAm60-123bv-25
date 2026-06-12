"""Tests for MemoryDatabase."""

import unittest
from src.db.backend.memory import MemoryDatabase
from src.db.backend.errors import TableNotFoundError, TableAlreadyExistsError, InvalidAgeError, DuplicateIDError


class TestMemoryDatabase(unittest.TestCase):
    def setUp(self):
        self.db = MemoryDatabase()

    def test_create_table(self):
        self.db.create_table("students", ("student_id", "first_name", "second_name", "age", "sex"))
        self.assertTrue(self.db._table_exists("students"))

    def test_create_table_already_exists(self):
        self.db.create_table("students", ("student_id", "first_name", "second_name", "age", "sex"))
        with self.assertRaises(TableAlreadyExistsError):
            self.db.create_table("students", ("student_id", "first_name", "second_name", "age", "sex"))

    def test_insert_valid_record(self):
        self.db.create_table("students", ("student_id", "first_name", "second_name", "age", "sex"))
        self.db.insert_record("students", {"student_id": 1, "first_name": "Иван", "second_name": "Петров", "age": 20, "sex": "м"})
        records = self.db.select_records("students")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["student_id"], 1)

    def test_insert_negative_age(self):
        self.db.create_table("students", ("student_id", "first_name", "second_name", "age", "sex"))
        with self.assertRaises(InvalidAgeError):
            self.db.insert_record("students", {"student_id": 1, "first_name": "Иван", "second_name": "Петров", "age": -5, "sex": "м"})

    def test_insert_duplicate_id(self):
        self.db.create_table("students", ("student_id", "first_name", "second_name", "age", "sex"))
        self.db.insert_record("students", {"student_id": 1, "first_name": "Иван", "second_name": "Петров", "age": 20, "sex": "м"})
        with self.assertRaises(DuplicateIDError):
            self.db.insert_record("students", {"student_id": 1, "first_name": "Петр", "second_name": "Сидоров", "age": 25, "sex": "м"})

    def test_select_with_filter(self):
        self.db.create_table("students", ("student_id", "first_name", "second_name", "age", "sex"))
        self.db.insert_record("students", {"student_id": 1, "first_name": "Иван", "second_name": "Петров", "age": 20, "sex": "м"})
        self.db.insert_record("students", {"student_id": 2, "first_name": "Мария", "second_name": "Иванова", "age": 22, "sex": "ж"})
        records = self.db.select_records("students", first_name="Мария")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["student_id"], 2)

    def test_select_missing_table(self):
        with self.assertRaises(TableNotFoundError):
            self.db.select_records("students")