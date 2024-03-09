import json
import os
import subprocess
import time
from pymongo import MongoClient


class MongoDBManager:
    def __init__(self, config_file='config.json'):
        self.config = self.load_config(config_file)
        self.client = None
        self.server_process = None
        self.is_server_created = False
        self.is_server_running = False

    def load_config(self, config_file):
        with open(config_file) as f:
            config = json.load(f)
        return config

    def create_database_server_folder(self):
        if not self.is_server_created and not self.is_server_running:
            data_dir = self.config.get('data_dir')
            os.makedirs(data_dir, exist_ok=True)
            self.is_server_created = True
            print("Server created successfully.")
        else:
            print("Server already created or running. Cannot create again.")

    def start_server(self):
        if self.is_server_created and not self.is_server_running:
            # Start the MongoDB server using subprocess.Popen
            data_dir = self.config.get('data_dir')
            try:
                self.server_process = subprocess.Popen(['mongod', '--dbpath', data_dir, '--bind_ip', '127.0.0.1'])
                print("Server started successfully.")
                time.sleep(2)  # Allow some time for the server to start
                self.is_server_running = True
                self.initialize_databases()
            except Exception as e:
                print(f"Error starting the server: {e}")
                self.is_server_running = False
        else:
            print("Server is not created or is already running.")

    def initialize_databases(self):
        if self.is_server_running:
            # Connect to the MongoDB server
            self.client = MongoClient('localhost', self.config.get('port', 27017))

            # Create necessary users and roles in the admin database if they do not exist
            admin_db = self.client.admin
            if not admin_db.command('usersInfo', 'admin')['users']:
                admin_db.command('createUser', 'admin', pwd='adminpass', roles=['userAdminAnyDatabase'])
            if not admin_db.command('usersInfo', 'configuser')['users']:
                admin_db.command('createUser', 'configuser', pwd='configpass', roles=['readWriteAnyDatabase'])

            # Create necessary users and roles in the config database if they do not exist
            config_db = self.client.config
            if not config_db.command('usersInfo', 'configuser')['users']:
                config_db.command('createUser', 'configuser', pwd='configpass', roles=['readWrite'])

            print("Databases initialized.")
        else:
            print("Server is not running. Cannot initialize databases.")

    def stop_server(self):
        if self.is_server_running:
            # Close the MongoDB client connection
            if self.client:
                self.client.close()

            # Stop the MongoDB server
            try:
                self.server_process.terminate()
                self.server_process.wait()  # Ensure the process is fully terminated
                print("Server stopped successfully.")
                self.is_server_running = False
            except Exception as e:
                print(f"Error stopping the server: {e}")
        else:
            print("Server is not running.")

    def connect_to_database(self):
        if self.is_server_running:
            return self.client[self.config['database']]
        else:
            print("Server is not running. Cannot connect to the database.")

    def add_user(self, database, username, password, roles):
        if self.is_server_running:
            db = self.client[database]
            try:
                db.command('createUser', username, pwd=password, roles=roles)
                print(f"User '{username}' added successfully to database '{database}'.")
            except Exception as e:
                print(f"Error adding user: {e}")
        else:
            print("Server is not running. Cannot add user.")

    def read_users(self, database):
        if self.is_server_running:
            db = self.client[database]
            users_info = db.command('usersInfo')
            users = [user['user'] for user in users_info['users']]
            print(f"Users in database '{database}': {', '.join(users)}")
        else:
            print("Server is not running. Cannot read users.")

    def update_user_password(self, database, username, new_password):
        if self.is_server_running:
            db = self.client[database]
            try:
                db.command('updateUser', username, pwd=new_password)
                print(f"Password updated successfully for user '{username}' in database '{database}'.")
            except Exception as e:
                print(f"Error updating password: {e}")
        else:
            print("Server is not running. Cannot update password.")

    def delete_user(self, database, username):
        if self.is_server_running:
            db = self.client[database]
            try:
                db.command('dropUser', username)
                print(f"User '{username}' deleted successfully from database '{database}'.")
            except Exception as e:
                print(f"Error deleting user: {e}")
        else:
            print("Server is not running. Cannot delete user.")

    def main_menu(self):
        while True:
            print(
                "\n1. Create Database Folder\n2. Start Server\n3. Stop Server\n4. Add User\n5. Read Users\n6. Update User Password\n7. Delete User\n8. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.create_database_server_folder()
            elif choice == '2':
                self.start_server()
            elif choice == '3':
                self.stop_server()
            elif choice == '4':
                database = input("Enter database name: ")
                username = input("Enter username: ")
                password = input("Enter password: ")
                roles = input("Enter roles (comma-separated): ").split(',')
                self.add_user(database, username, password, roles)
            elif choice == '5':
                database = input("Enter database name: ")
                self.read_users(database)
            elif choice == '6':
                database = input("Enter database name: ")
                username = input("Enter username: ")
                new_password = input("Enter new password: ")
                self.update_user_password(database, username, new_password)
            elif choice == '7':
                database = input("Enter database name: ")
                username = input("Enter username: ")
                self.delete_user(database, username)
            elif choice == '8':
                if self.is_server_running:
                    self.stop_server()  # Stop MongoDB server before exiting
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    manager = MongoDBManager()
    manager.main_menu()
