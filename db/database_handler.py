import os
import sqlite3
import psycopg
import mysql.connector
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file
load_dotenv()

# Create logs directory if it does not exist
logs_dir = 'logs'
os.makedirs(logs_dir, exist_ok=True)

# Configure logger
logger.add(os.path.join(logs_dir, "database_handler.log"), rotation="1 week", retention="1 month", level="DEBUG")

class DatabaseHandler:
    """
    A class to handle connections and operations for various types of databases.
    
    Supported databases: SQLite, PostgreSQL, MySQL, MongoDB.
    """
    
    def __init__(self, db_type=None, db_url=None):
        """
        Initialize the database handler with the provided db_type and db_url.
        
        Parameters:
        - db_type (str): The type of the database ('sqlite', 'postgresql', 'mysql', 'mongodb').
        - db_url (str): The connection URL for the database.
        
        If no db_type is provided, defaults to the environment variable DATABASE_TYPE.
        """
        self.db_type = db_type or os.getenv('DATABASE_TYPE', 'sqlite')
        self.db_url = db_url or os.getenv('DATABASE_URL', None)
        self.conn = None
        self.cursor = None
        self.db = None

    def connect(self):
        """
        Establish a connection to the database based on the specified db_type.
        
        Raises:
        - ValueError: If the provided or default db_type is unsupported.
        """
        try:
            if self.db_type == 'sqlite':
                self._connect_sqlite()
            elif self.db_type == 'postgresql':
                self._connect_postgresql()
            elif self.db_type == 'mysql':
                self._connect_mysql()
            elif self.db_type == 'mongodb':
                self._connect_mongodb()
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")
        except Exception as e:
            logger.error(f"Failed to connect: {e}")

    def _connect_sqlite(self):
        """
        Connect to a SQLite database.
        
        SQLite uses a file-based approach for storage. The database URL should be in the format `sqlite:///path_to_db/my_database.db`.
        """
        try:
            self.conn = sqlite3.connect(self.db_url.split(':///')[-1])
            self.cursor = self.conn.cursor()
            logger.info("Connected to SQLite database.")
        except sqlite3.Error as e:
            logger.error(f"SQLite connection failed: {e}")

    def _connect_postgresql(self):
        """
        Connect to a PostgreSQL database.
        
        The database URL should be in the format `postgres://user:password@localhost/mydatabase`.
        """
        try:
            self.conn = psycopg.connect(self.db_url)
            self.cursor = self.conn.cursor()
            logger.info("Connected to PostgreSQL database.")
        except psycopg.Error as e:
            logger.error(f"PostgreSQL connection failed: {e}")

    def _connect_mysql(self):
        """
        Connect to a MySQL database.
        
        The database URL should be in the format `mysql://username:password@localhost/dbname`.
        """
        try:
            self.conn = mysql.connector.connect(self.db_url)
            self.cursor = self.conn.cursor()
            logger.info("Connected to MySQL database.")
        except mysql.connector.Error as e:
            logger.error(f"MySQL connection failed: {e}")

    def _connect_mongodb(self):
        """
        Connect to a MongoDB database.
        
        The database URL should be in the format `mongodb://username:password@localhost:27017/mydatabase`.
        """
        try:
            client = MongoClient(self.db_url)
            self.db = client.get_database()
            logger.info("Connected to MongoDB.")
        except pymongo.errors.ConnectionError as e:
            logger.error(f"MongoDB connection failed: {e}")

    def execute_query(self, query, params=()):
        """
        Execute a query for SQL-based databases (SQLite, PostgreSQL, MySQL).
        
        Parameters:
        - query (str): The SQL query to execute.
        - params (tuple): Parameters to be used with the query.
        
        Returns:
        - list: A list of tuples containing the query results.
        
        Raises:
        - NotImplementedError: If attempting to execute SQL queries on MongoDB.
        """
        if self.db_type in ['sqlite', 'postgresql', 'mysql']:
            try:
                self.cursor.execute(query, params)
                self.conn.commit()
                return self.cursor.fetchall()
            except (sqlite3.Error, psycopg.Error, mysql.connector.Error) as e:
                logger.error(f"Error executing query: {e}")
                return None
        else:
            logger.error("MongoDB does not support SQL-style queries.")
            raise NotImplementedError("MongoDB does not support SQL-style queries.")

    def insert(self, table, data):
        """
        Insert data into a specified table.
        
        Parameters:
        - table (str): The name of the table.
        - data (dict): A dictionary where keys are column names and values are the data to insert.
        
        Raises:
        - NotImplementedError: If trying to insert into MongoDB, as MongoDB requires different handling.
        """
        if self.db_type == 'mongodb':
            try:
                self.db[table].insert_one(data)
                logger.info(f"Document inserted into {table}.")
            except Exception as e:
                logger.error(f"Error inserting document into {table}: {e}")
        else:
            try:
                columns = ', '.join(data.keys())
                placeholders = ', '.join('%s' for _ in data)  # Works for both PostgreSQL and MySQL
                query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
                self.execute_query(query, tuple(data.values()))
            except Exception as e:
                logger.error(f"Error inserting data into {table}: {e}")

    def fetch_all(self, table):
        """
        Fetch all records from a specified table.
        
        Parameters:
        - table (str): The name of the table.
        
        Returns:
        - list: A list of records from the table. For MongoDB, this is a list of documents.
        """
        try:
            if self.db_type == 'mongodb':
                return list(self.db[table].find())
            else:
                query = f"SELECT * FROM {table}"
                return self.execute_query(query)
        except Exception as e:
            logger.error(f"Error fetching records from {table}: {e}")
            return None

    def update(self, table, data, where_clause, where_params):
        """
        Update records in a specified table.
        
        Parameters:
        - table (str): The name of the table.
        - data (dict): A dictionary where keys are column names and values are the new values.
        - where_clause (str): The WHERE clause for the update query.
        - where_params (tuple): Parameters for the WHERE clause.
        
        Raises:
        - NotImplementedError: MongoDB requires different update functionality.
        """
        if self.db_type == 'mongodb':
            logger.error("MongoDB requires different update functionality.")
            raise NotImplementedError("Use MongoDB's update functionality.")
        else:
            try:
                set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
                query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
                self.execute_query(query, tuple(data.values()) + tuple(where_params))
            except Exception as e:
                logger.error(f"Error updating records in {table}: {e}")

    def delete(self, table, where_clause, where_params):
        """
        Delete records from a specified table.
        
        Parameters:
        - table (str): The name of the table.
        - where_clause (str): The WHERE clause for the delete query.
        - where_params (tuple): Parameters for the WHERE clause.
        
        Raises:
        - NotImplementedError: MongoDB requires different deletion functionality.
        """
        if self.db_type == 'mongodb':
            try:
                self.db[table].delete_many(where_clause)
                logger.info(f"Documents deleted from {table}.")
            except Exception as e:
                logger.error(f"Error deleting documents from {table}: {e}")
        else:
            try:
                query = f"DELETE FROM {table} WHERE {where_clause}"
                self.execute_query(query, where_params)
            except Exception as e:
                logger.error(f"Error deleting records from {table}: {e}")

    def close(self):
        """
        Close the database connection for SQL databases (SQLite, PostgreSQL, MySQL).
        MongoDB connections are managed differently and do not require explicit closing.
        """
        if self.db_type in ['sqlite', 'postgresql', 'mysql']:
            try:
                if self.conn:
                    self.conn.close()
                    logger.info(f"{self.db_type.capitalize()} connection closed.")
            except Exception as e:
                logger.error(f"Error closing connection: {e}")
