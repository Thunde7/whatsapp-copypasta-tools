"""
Database module
"""
import json
import logging
import os
from pyravendb.store import document_store
from pyravendb.changes.observers import ActionObserver
from pyravendb.custom_exceptions.exceptions import InvalidOperationException, NotSupportedException


# ================================================================================

CERT_FILE = os.path.join(os.getcwd(), os.environ.get("DB_CERT_PATH", ""))
KEY_FILE = os.path.join(os.getcwd(), os.environ.get("DB_KEY_PATH", ""))
DB_URL = os.environ.get("DB_URL", 'https://127.0.0.1')
COMMON_DATE_FORMAT = "%Y-%m-%d_%H-%M"

# ================================================================================


class DbDocument:
    """
    DbDoc base class
    """
    def __init__(self, data=None):
        pass

    def __str__(self):
        return json.dumps(self.__dict__)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, item):
        return getattr(self, item) if hasattr(self, item) else None

    def __contains__(self, item):
        return hasattr(self, item)

    def __delitem__(self, key):
        delattr(self, key)

    def update(self, data):
        """
        Update the object with the data
        """
        if not isinstance(data, dict):
            try:
                data = data.__dict__
            except AttributeError as exc:
                raise Exception("can only proces dictionaties and raven docs") from exc
        for key, val in data.items:
            setattr(self, key, val)

    def dump(self):
        """
        Dump the object to a dictionary
        """
        for i in list(self.__dict__.keys()):
            print(i, self[i])


class Pasta(DbDocument):
    """
    CopyPasta Class
    """


class User(DbDocument):
    """
    User Class
    """


class Result(DbDocument):
    """
    Result Class
    """


# -------------------------------------------------------------------------------


class DbTable:
    """
    DB Table wrapper
    """
    dbname = "" # Placeholder for future use
    objType = DbDocument # Placeholder for future use
    all_observer = None # might be initialized in the future

    def __init__(self, cloud: bool = False):
        try:
            self.logger = logging.getLogger(
                __name__ + "." + self.dbname)
            self.is_cloud = cloud
            self.cert = (CERT_FILE, KEY_FILE)
            self.url = DB_URL
            self.store = document_store.DocumentStore(urls=[self.url],
                                                      database=self.dbname,
                                                      certificate=self.cert
                                                      )
            self.store.initialize()
        except ValueError as exc:
            self.logger.exception("Failed to initialize the store - %s", exc)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.store.close()

    @staticmethod
    def add_ids(query_result, session):
        """
        Add the id to the result
        """
        results = {}
        for res in query_result:
            _id = session.advanced.get_document_id(res)
            if not _id.startswith("Raven"):
                results[_id] = res
        return results

    def observer(self, callback=None, on_error=None, on_completed=None):
        """
        Create an observer for the changes
        """
        self.all_observer = self.store.changes().for_all_documents()
        self.all_observer.subscribe(ActionObserver(
            on_next=callback, on_error=on_error, on_completed=on_completed))
        self.all_observer.ensure_subscribe_now()

    def get_all(self):
        """
        Get all the documents in the table
        """
        with self.store.open_session() as session:
            query_result = list(session.query)
            result = self.add_ids(query_result, session)
        return result

    def get_by_id(self, _id):
        """
        Get a document by id
        """
        with self.store.open_session() as session:
            query_result = session.load(_id, object_type=self.objType)
        return query_result

    def get_by_field(self, field, value, inverse=False):
        """
        Get a document by field
        """
        with self.store.open_session() as session:
            if inverse:
                result = list(session.query.where_not_equals(field, value))
            else:
                result = list(session.query.where_equals(field, value))
        return self.add_ids(result, session)

    def get_field_exists(self, field_name):
        """
        Check if a field exists
        """
        with self.store.open_session() as session:
            result = list(session.query.where_exists(field_name))
        return self.add_ids(result, session)

    def create(self, data, _id=None):
        """
        Create a new document
        """
        with self.store.open_session() as session:
            obj = self.objType()
            obj.update(data)
            session.store(obj, key=_id)
            session.save_changes()
            return session.advanced.get_document_id(obj)

    def update(self, data, _id):
        """
        Update a document
        """
        if isinstance(data, dict):
            self.create(data, _id)
        else:
            self.create(data.__dict__, _id)

    def delete_by_id(self, ids):
        """
        Delete a document by id
        """
        if isinstance(ids, str):
            ids = [ids]
        with self.store.open_session() as session:
            for _id in ids:
                self.logger.debug("deleting %s", _id)
                if _id is not None:
                    session.delete(_id)
            session.save_changes()

# -------------------------------------------------------------------------------


class TablePastas(DbTable):
    """
    CopyPastas Table
    """

    dbname = "Pastas"
    objType = Pasta

    def fuzzy_search(self, subtext: str):
        """
        Fuzzy search for the pastas that contain the subtext
        """
        try:
            with self.store.open_session() as session:
                query = session.query.search('text', subtext)
                return list(query) if query else None
        except IndexError:
            return None
        except (InvalidOperationException, NotSupportedException, ValueError) as exc:
            logging.exception("get unfinished by rater error - %s", exc)
            return None


class TableUsers(DbTable):
    """
    Users Table
    """

    dbname = "Stats"
    objType = User

    def get_sent_by(self, number: str):
        """
        Get the sent pastas by the user with the number
        """
        try:
            with self.store.open_session() as session:
                query = session.query.where_equals('number', number)
                return list(query) if query else None
        except IndexError:
            return None
        except (InvalidOperationException, NotSupportedException, ValueError) as exc:
            logging.exception("get unfinished by rater error - %s", exc)
            return None


class TableResults(DbTable):
    """
    Search Results cache Table
    """
    dbname = "Cache"
    objType = Result
