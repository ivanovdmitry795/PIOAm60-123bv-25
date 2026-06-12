"""Tests for MemoryDatabase."""

import unittest
from src.db.backend.memory import MemoryDatabase
from src.db.backend.errors import TableNotFoundError, TableAlreadyExistsError


class TestMemoryDatabase(unittest.TestCase):
    def setUp(self):
        self.db = MemoryDatabase()

    def test_create_table(self):
        self.db.create_table("students", ("id", "name"))
        self.assertTrue(self.db._table_exists("students"))

    def test_create_table_already_exists(self):
        self.db.create_table("students", ("id", "name"))
        with self.assertRaises(TableAlreadyExistsError):
            self.db.create_table("students", ("id", "name"))

    def test_insert_record(self):
        self.db.create_table("students", ("id", "name"))
        self.db.insert_record("students", {"id": 1, "name": "Иван"})
        records = self.db.select_records("students")
        self.assertEqual(records, [{"id": 1, "name": "Иван"}])

    def test_select_with_filter(self):
        self.db.create_table("students", ("id", "name"))
        self.db.insert_record("students", {"id": 1, "name": "Иван"})
        self.db.insert_record("students", {"id": 2, "name": "Мария"})
        records = self.db.select_records("students", name="Мария")
        self.assertEqual(records, [{"id": 2, "name": "Мария"}])

    def test_select_missing_table(self):
        with self.assertRaises(TableNotFoundError):
            self.db.select_records("students")
