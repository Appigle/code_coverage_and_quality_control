import unittest
from unittest.mock import Mock, patch
from user import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Create mock for sqlite3.connect and cursor
        self.cursor_mock = Mock()
        self.conn_mock = Mock()
        self.conn_mock.cursor.return_value = self.cursor_mock

        self.cursor_mock.reset_mock()
        self.conn_mock.reset_mock()

        self.patcher = patch('sqlite3.connect', return_value=self.conn_mock)
        self.patcher.start()

        self.db = Database('test.db')

    def reset_mock(self):
        self.cursor_mock.reset_mock()
        self.conn_mock.reset_mock()

    def tearDown(self):
        self.patcher.stop()

    def test_init_creates_table(self):
        self.cursor_mock.execute.assert_called_with(
            'CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, name TEXT NOT NULL, age INTEGER CHECK (age >= 0))'
        )

    def test_insert_user(self):
        self.reset_mock()

        self.cursor_mock.lastrowid = 1

        result = self.db.insert_user("John", 30)

        self.cursor_mock.execute.assert_called_with(
            'INSERT INTO users (name, age) VALUES (?, ?)',
            ("John", 30)
        )
        self.conn_mock.commit.assert_called_once()
        self.assertEqual(result, 1)

    def test_get_user_found(self):
        self.reset_mock()

        expected_user = (1, "John", 30)
        self.cursor_mock.fetchone.return_value = expected_user

        result = self.db.get_user(1)

        self.cursor_mock.execute.assert_called_with(
            'SELECT * FROM users WHERE user_id = ?',
            (1,)
        )
        self.assertEqual(result, expected_user)

    def test_get_user_not_found(self):
        self.reset_mock()

        self.cursor_mock.fetchone.return_value = None

        result = self.db.get_user(1)

        self.cursor_mock.execute.assert_called_with(
            'SELECT * FROM users WHERE user_id = ?',
            (1,)
        )
        self.assertIsNone(result)

    def test_update_user_success(self):
        self.reset_mock()

        self.cursor_mock.rowcount = 1

        result = self.db.update_user(1, "John Updated", 31)

        self.cursor_mock.execute.assert_called_with(
            'UPDATE users SET name = ?, age = ? WHERE user_id = ?',
            ("John Updated", 31, 1)
        )
        self.conn_mock.commit.assert_called_once()
        self.assertTrue(result)

    def test_update_user_not_found(self):
        self.reset_mock()

        self.cursor_mock.rowcount = 0

        result = self.db.update_user(1, "John Updated", 31)

        self.cursor_mock.execute.assert_called_with(
            'UPDATE users SET name = ?, age = ? WHERE user_id = ?',
            ("John Updated", 31, 1)
        )
        self.conn_mock.commit.assert_called_once()
        self.assertFalse(result)

    def test_delete_user_success(self):
        self.reset_mock()

        self.cursor_mock.rowcount = 1

        result = self.db.delete_user(1)

        self.cursor_mock.execute.assert_called_with(
            'DELETE FROM users WHERE user_id = ?',
            (1,)
        )
        self.conn_mock.commit.assert_called_once()
        self.assertTrue(result)

    def test_delete_user_not_found(self):
        self.reset_mock()

        self.cursor_mock.rowcount = 0

        result = self.db.delete_user(1)

        self.cursor_mock.execute.assert_called_with(
            'DELETE FROM users WHERE user_id = ?',
            (1,)
        )
        self.conn_mock.commit.assert_called_once()
        self.assertFalse(result)

    def test_invalid_age(self):
        with self.assertRaises(ValueError):
            self.db.insert_user("John", -1)

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            self.db.insert_user("", 30)


if __name__ == '__main__':
    unittest.main()
