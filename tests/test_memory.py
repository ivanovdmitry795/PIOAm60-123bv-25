"""Unit tests for StudentTable class."""

import unittest
from src.db.backend.memory import StudentTable
from src.db.backend.errors import InvalidAgeError, DuplicateIDError


class TestMemory(unittest.TestCase):
    """Test cases for StudentTable."""
    
    def setUp(self):
        """Create a fresh table before each test."""
        self.student_table = StudentTable()
        self.assertIsInstance(self.student_table, StudentTable)
    
    def test_create_record_valid(self):
        """Test creating valid records."""
        test_data = (1, "John", "Doe", 20, "M")
        record = self.student_table.create_record(*test_data)
        self.assertEqual(record, test_data)
    
    def test_create_record_multiple(self):
        """Test creating multiple records."""
        records = [
            (1, "John", "Doe", 20, "M"),
            (2, "Jane", "Smith", 22, "F"),
            (3, "Bob", "Brown", 21, "M"),
        ]
        for test_data in records:
            record = self.student_table.create_record(*test_data)
            self.assertEqual(record, test_data)
    
    def test_create_record_negative_age(self):
        """Test negative age raises InvalidAgeError."""
        with self.assertRaises(InvalidAgeError):
            self.student_table.create_record(1, "John", "Doe", -5, "M")
    
    def test_create_record_duplicate_id(self):
        """Test duplicate ID raises DuplicateIDError."""
        self.student_table.create_record(1, "John", "Doe", 20, "M")
        with self.assertRaises(DuplicateIDError):
            self.student_table.create_record(1, "Jane", "Smith", 22, "F")
    
    def test_select_record_no_filters(self):
        """Test select returns all records."""
        records = [
            (1, "John", "Doe", 20, "M"),
            (2, "Jane", "Smith", 22, "F"),
        ]
        for r in records:
            self.student_table.create_record(*r)
        
        result = self.student_table.select_record()
        self.assertEqual(result, records)
    
    def test_select_record_by_id(self):
        """Test filter by student_id."""
        records = [
            (1, "John", "Doe", 20, "M"),
            (2, "Jane", "Smith", 22, "F"),
            (3, "Bob", "Brown", 21, "M"),
        ]
        for r in records:
            self.student_table.create_record(*r)
        
        result = self.student_table.select_record(student_id=2)
        self.assertEqual(result, [records[1]])
    
    def test_select_record_by_first_name(self):
        """Test filter by first_name."""
        records = [
            (1, "John", "Doe", 20, "M"),
            (2, "Jane", "Smith", 22, "F"),
            (3, "John", "Brown", 21, "M"),
        ]
        for r in records:
            self.student_table.create_record(*r)
        
        result = self.student_table.select_record(first_name="John")
        self.assertEqual(result, [records[0], records[2]])
    
    def test_select_record_by_age(self):
        """Test filter by age."""
        records = [
            (1, "John", "Doe", 20, "M"),
            (2, "Jane", "Smith", 22, "F"),
            (3, "Bob", "Brown", 20, "M"),
        ]
        for r in records:
            self.student_table.create_record(*r)
        
        result = self.student_table.select_record(age=20)
        self.assertEqual(result, [records[0], records[2]])
    
    def test_select_record_by_sex(self):
        """Test filter by sex."""
        records = [
            (1, "John", "Doe", 20, "M"),
            (2, "Jane", "Smith", 22, "F"),
            (3, "Bob", "Brown", 21, "M"),
        ]
        for r in records:
            self.student_table.create_record(*r)
        
        result = self.student_table.select_record(sex="M")
        self.assertEqual(result, [records[0], records[2]])
    
    def test_select_record_multiple_filters(self):
        """Test filter by multiple fields."""
        records = [
            (1, "John", "Doe", 20, "M"),
            (2, "John", "Smith", 22, "M"),
            (3, "Bob", "Doe", 20, "M"),
        ]
        for r in records:
            self.student_table.create_record(*r)
        
        result = self.student_table.select_record(first_name="John", second_name="Doe")
        self.assertEqual(result, [records[0]])
    
    def test_select_record_no_match(self):
        """Test filter with no matches returns empty list."""
        self.student_table.create_record(1, "John", "Doe", 20, "M")
        
        result = self.student_table.select_record(first_name="Nonexistent")
        self.assertEqual(result, [])
    
    def test_select_record_empty_table(self):
        """Test select on empty table returns empty list."""
        result = self.student_table.select_record()
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()