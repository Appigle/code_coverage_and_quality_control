from user import Database, UserService, DatabaseError
import sys
from typing import Optional


def get_integer_input(prompt: str) -> Optional[int]:
    """Safely get integer input from user"""
    try:
        return int(input(prompt))
    except ValueError:
        print("Please enter a valid number")
        return None


def main():
    try:
        db = Database('users.db')
        user_service = UserService(db)

        while True:
            print("\n=== User Management System ===")
            print("1. Get user")
            print("2. Create user")
            print("3. Update user")
            print("4. Delete user")
            print("5. Exit")

            choice = get_integer_input("\nEnter your choice (1-5): ")
            if not choice:
                continue

            if choice == 5:
                break

            try:
                if choice == 1:
                    if user_id := get_integer_input("Enter user ID: "):
                        user_data, status_code = user_service.get_user(user_id)
                        print(f"Response: {
                              user_data} (Status Code: {status_code})")

                elif choice == 2:
                    name = input("Enter user name: ").strip()
                    if age := get_integer_input("Enter user age: "):
                        user_data, status_code = user_service.create_user(
                            name, age)
                        print(f"Response: {
                              user_data} (Status Code: {status_code})")

                elif choice == 3:
                    if user_id := get_integer_input("Enter user ID: "):
                        name = input("Enter new name: ").strip()
                        if age := get_integer_input("Enter new age: "):
                            user_data, status_code = user_service.update_user(
                                user_id, name, age)
                            print(f"Response: {
                                  user_data} (Status Code: {status_code})")

                elif choice == 4:
                    if user_id := get_integer_input("Enter user ID: "):
                        user_data, status_code = user_service.delete_user(
                            user_id)
                        print(f"Response: {
                              user_data} (Status Code: {status_code})")

            except DatabaseError as e:
                print("An error occurred while accessing the database")

    except Exception as e:
        print("An unexpected error occurred")
        sys.exit(1)


if __name__ == '__main__':
    main()
