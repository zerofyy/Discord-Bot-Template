from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from pymongo.collection import InsertOneResult, InsertManyResult, DeleteResult, UpdateResult

import os
import dotenv


class DB:
    """ Static wrapper for the Mongo database. """

    client: MongoClient = None
    database: Database = None


    @classmethod
    def setup(cls, db_url: str = None) -> None:
        """
        Set up the Mongo database.

        Arguments:
             db_url: A MongoDB connection url. Defaults to loading from the "DB_URL" environmental variable.

        Raises:
            ValueError: If "DB_URL" is not found in the environment variables.
        """

        if db_url is None:
            dotenv.load_dotenv()
            db_url = os.getenv('DB_URL')

            if not db_url:
                raise ValueError('DB_URL not found in environment variables.')

        cls.client = MongoClient(db_url)
        cls.database = cls.client['Database']


    @classmethod
    def find(cls, collection: str, query: dict[str, ...], find_many: bool = False) \
            -> tuple[dict[str, ...], ...] | dict[str, ...] | None:
        """
        Find documents in a database collection.

        Arguments:
             collection: Name of the database collection.
             query: The search query.
             find_many: Whether to find all documents that satisfy the query or stop at the first one.

        Returns:
            The documents or None if not found.
        """

        if find_many:
            return tuple(cls.database[collection].find(query)) or None

        return cls.database[collection].find_one(query)


    @classmethod
    def insert(cls, collection: str, data: dict[str, ...] | list[dict[str, ...]]) \
            -> InsertOneResult | InsertManyResult:
        """
        Insert documents to a database collection.

        Arguments:
            collection: Name of the database collection.
            data: The document(s) to insert.

        Returns:
            The result of inserting documents.
        """

        if isinstance(data, list):
            return cls.database[collection].insert_many(data)

        return cls.database[collection].insert_one(data)


    @classmethod
    def delete(cls, collection: str, query: dict[str, ...], delete_many: bool = False) -> DeleteResult:
        """
        Delete documents from a database collection.

        Arguments:
             collection: Name of the database collection.
             query: The search query.
             delete_many: Whether to delete all documents that satisfy the query or just the first one.

        Returns:
            The result of deleting documents.
        """

        if delete_many:
            return cls.database[collection].delete_many(query)

        return cls.database[collection].delete_one(query)


    @classmethod
    def update(cls, collection: str, query: dict[str, ...], updates: dict[str, dict[str, ...]],
               update_many: bool = False, upsert: bool = False) -> UpdateResult:
        """
        Update documents in a database collection.

        Update modifications: https://www.mongodb.com/docs/upcoming/reference/mql/update/#std-label-update-operators

        Arguments:
            collection: Name of the database collection.
            query: The search query.
            updates: Update modifications to apply onto the documents.
            update_many: Whether to update all documents that satisfy the query or just the first one.
            upsert: Whether to insert a new document if no documents satisfy the query.

        Returns:
            The result of updating documents.
        """

        if update_many:
            return cls.database[collection].update_many(query, updates, upsert = upsert)

        return cls.database[collection].update_one(query, updates, upsert = upsert)


__all__ = ['DB']
