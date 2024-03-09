# MongoDBManager Notes

## Overview
The `MongoDBManager` class is designed to manage MongoDB server instances, initialize databases, and perform various operations on users within these databases. The program provides a simple command-line interface (CLI) through the `main_menu` method, allowing users to create databases, start and stop the MongoDB server, add, read, update, and delete users, and exit the program.

## Class Structure
### Initialization
- The class constructor (`__init__`) initializes the MongoDBManager with default values and loads configuration settings from a JSON file (`config.json` by default).

### Configuration
- `load_config(config_file)`: Loads the MongoDB configuration from the specified JSON file.

### Server Management
- `create_database_server_folder()`: Creates a server data directory for MongoDB if it doesn't exist.
- `start_server()`: Starts the MongoDB server using `subprocess.Popen` and initializes databases.
- `initialize_databases()`: Connects to the MongoDB server and creates necessary users and roles.
- `stop_server()`: Stops the MongoDB server and closes the client connection.

### Database Operations
- `connect_to_database()`: Connects to the specified database.
- `add_user(database, username, password, roles)`: Adds a user to the specified database with the given roles.
- `read_users(database)`: Reads and displays the users in the specified database.
- `update_user_password(database, username, new_password)`: Updates the password for a user in the specified database.
- `delete_user(database, username)`: Deletes a user from the specified database.

### User Interface
- `main_menu()`: Provides a command-line interface for users to interact with the program.

## Usage
1. Create an instance of `MongoDBManager`.
2. Call the `main_menu` method to interact with the MongoDB server and databases through the command-line interface.

## Configuration File (`config.json`)
The configuration file should contain the following parameters:
- `data_dir`: The directory where MongoDB data is stored.
- `port`: The MongoDB server port (default: 27017).
- Other MongoDB connection parameters.

## Example Usage
```python
if __name__ == "__main__":
    manager = MongoDBManager()
    manager.main_menu()
