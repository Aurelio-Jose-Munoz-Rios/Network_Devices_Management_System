from __future__ import annotations

import mysql.connector
from mysql.connector import Error


class DatabaseConnector:
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None

    def connect(self) -> None:
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            if self.connection.is_connected():
                print('Connected to MariaDB/MySQL.')
        except Error as error:
            raise RuntimeError(f'Connection error: {error}') from error

    def disconnect(self) -> None:
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print('Disconnected from MariaDB/MySQL.')

    def execute_query(self, query: str, params: tuple | None = None) -> int:
        if not self.connection or not self.connection.is_connected():
            raise RuntimeError('There is no active database connection.')
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor.lastrowid
        except Error as error:
            self.connection.rollback()
            raise RuntimeError(f'Error executing query: {error}') from error
        finally:
            cursor.close()

    def fetch_all(self, query: str, params: tuple | None = None) -> list[dict]:
        if not self.connection or not self.connection.is_connected():
            raise RuntimeError('There is no active database connection.')
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except Error as error:
            raise RuntimeError(f'Error fetching rows: {error}') from error
        finally:
            cursor.close()

    def fetch_one(self, query: str, params: tuple | None = None) -> dict | None:
        if not self.connection or not self.connection.is_connected():
            raise RuntimeError('There is no active database connection.')
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            return cursor.fetchone()
        except Error as error:
            raise RuntimeError(f'Error fetching row: {error}') from error
        finally:
            cursor.close()
