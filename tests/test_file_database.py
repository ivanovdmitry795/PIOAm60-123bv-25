"""Tests for FileDatabase."""

import tempfile
import unittest
from src.db.backend.file import FileDatabase
from src.db.backend.errors import TableNotFoundError, InvalidAgeError, DuplicateIDError


class TestFileDatabase(unittest.TestCase):
    def test_data_saved_between_instances(self):
        with tempfile.TemporaryDirectory() as d:
            db1 = FileDatabase(d)
            db1.create_table("students", ("student_id", "first_name", "second_name", "age", "sex"))
            db1.insert_record("students", {"student_id": 1, "first_name": "Иван", "second_name": "Петров", "age": 20, "sex": "м"})

            db2 = FileDatabase(d)
            records = db2.select_records("students")
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["student_id"], 1)

    def test_select_with_filter(self):
        with tempfile.TemporaryDirectory() as d:
            db = FileDatabase(d)
            db.create_table("students", ("student_id", "first_name", "second_name", "age", "sex"))
            db.insert_record("students", {"student_id": 1, "first_name": "Иван", "second_name": "Петров", "age": 20, "sex": "м"})
            db.insert_record("students", {"student_id": 2, "first_name": "Мария", "second_name": "Иванова", "age": 22, "sex": "ж"})

            records = db.select_records("students", first_name="Мария")
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["student_id"], 2)

    def test_select_missing_table(self):
        with tempfile.TemporaryDirectory() as d:
            db = FileDatabase(d)
            with self.assertRaises(TableNotFoundError):
                db.select_records("students")

    def test_insert_negative_age(self):
        with tempfile.TemporaryDirectory() as d:
            db = FileDatabase(d)
            db.create_table("students", ("student_id", "first_name", "second_name", "age", "sex"))
            with self.assertRaises(InvalidAgeError):
                db.insert_record("students", {"student_id": 1, "first_name": "Иван", "second_name": "Петров", "age": -5, "sex": "м"})

    def test_insert_duplicate_id(self):
        with tempfile.TemporaryDirectory() as d:
            db = FileDatabase(d)
            db.create_table("students", ("student_id", "first_name", "second_name", "age", "sex"))
            db.insert_record("students", {"student_id": 1, "first_name": "Иван", "second_name": "Петров", "age": 20, "sex": "м"})
            with self.assertRaises(DuplicateIDError):
                db.insert_record("students", {"student_id": 1, "first_name": "Петр", "second_name": "Сидоров", "age": 25, "sex": "м"})
