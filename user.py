import sqlite3
from typing import Tuple, Optional, Dict, Any
from contextlib import contextmanager


class DatabaseError(Exception):
    """Custom exception for database operations"""
    pass


class User:
    def __init__(self, user_id: int, name: str, age: int):
        if not isinstance(age, int) or age < 0:
            raise ValueError("Age must be a positive integer")
        if not name.strip():
            raise ValueError("Name cannot be empty")

        self.user_id = user_id
        self.name = name
        self.age = age


class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self._init_db()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
        except sqlite3.Error as e:
            raise DatabaseError(f"Database operation failed: {e}")
        finally:
            conn.close()

    def _init_db(self) -> None:
        """Initialize the database with required tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, name TEXT NOT NULL, age INTEGER CHECK (age >= 0))'
            )
            conn.commit()

    def insert_user(self, name: str, age: int) -> int:
        """Insert a new user and return their ID"""
        if not isinstance(age, int) or age < 0:
            raise ValueError("Age must be a positive integer")
        if not name.strip():
            raise ValueError("Name cannot be empty")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
            conn.commit()
            return cursor.lastrowid

    def get_user(self, user_id: int) -> Optional[Tuple[int, str, int]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            return cursor.fetchone()

    def update_user(self, user_id: int, name: str, age: int) -> bool:
        if not isinstance(age, int) or age < 0:
            raise ValueError("Age must be a positive integer")
        if not name.strip():
            raise ValueError("Name cannot be empty")

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE users SET name = ?, age = ? WHERE user_id = ?', (name, age, user_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_user(self, user_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
            conn.commit()
            return cursor.rowcount > 0


class UserService:
    def __init__(self, db: Database):
        self.db = db

    def create_user(self, name: str, age: int) -> Tuple[Dict[str, Any], int]:
        try:
            user_id = self.db.insert_user(name, age)
            return {"user_id": user_id, "name": name, "age": age}, 201
        except ValueError as e:
            return {"error": str(e)}, 400
        except DatabaseError as e:
            return {"error": "Internal server error"}, 500

    def get_user(self, user_id: int) -> Tuple[Dict[str, Any], int]:
        user = self.db.get_user(user_id)
        if user:
            return {"user_id": user[0], "name": user[1], "age": user[2]}, 200
        else:
            return {"error": "User not found"}, 404

    def update_user(self, user_id: int, name: str, age: int) -> Tuple[Dict[str, Any], int]:
        try:
            if self.db.update_user(user_id, name, age):
                return {"user_id": user_id, "name": name, "age": age}, 200
            return {"error": "User not found"}, 404
        except ValueError as e:
            return {"error": str(e)}, 400
        except DatabaseError as e:
            return {"error": "Internal server error"}, 500

    def delete_user(self, user_id: int) -> Tuple[Dict[str, Any], int]:
        try:
            if self.db.delete_user(user_id):
                return {"message": "User deleted successfully"}, 200
            return {"error": "User not found"}, 404
        except DatabaseError as e:
            return {"error": "Internal server error"}, 500
