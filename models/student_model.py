import uuid
from datetime import datetime, timezone
import pymongo
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from bson.objectid import ObjectId

class StudentModel:
    """
    Data model for Student Profile persistence.
    Supports MongoDB database operations with a built-in graceful fallback
    to local memory storage if MongoDB is offline or unconfigured.
    """
    _in_memory_store = {}  # Global dictionary for fallback storage when DB is offline

    def __init__(self, mongodb_uri="mongodb://localhost:27017/student_career_db", db_name="student_career_db"):
        self.mongodb_uri = mongodb_uri
        self.db_name = db_name
        self.client = None
        self.db = None
        self.collection = None
        self.using_fallback = False
        self._connect()

    def _connect(self):
        """Attempts connection to MongoDB server with a short timeout."""
        try:
            self.client = pymongo.MongoClient(self.mongodb_uri, serverSelectionTimeoutMS=2000)
            # Ping the server to check connectivity
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            self.collection = self.db['students']
            self.using_fallback = False
        except (ConnectionFailure, ServerSelectionTimeoutError, Exception) as e:
            # Fallback mode enabled if database is not reachable
            self.using_fallback = True
            self.client = None
            self.db = None
            self.collection = None

    def is_db_connected(self):
        """Returns True if MongoDB is connected, False if operating in fallback mode."""
        if self.using_fallback:
            return False
        try:
            self.client.admin.command('ping')
            return True
        except Exception:
            self.using_fallback = True
            return False

    def save_student(self, student_data):
        """
        Saves a new student document or creates a record in fallback store.
        Returns the student_id string.
        """
        now = datetime.now(timezone.utc).isoformat()
        student_data['created_at'] = student_data.get('created_at', now)
        student_data['updated_at'] = now

        if not self.is_db_connected():
            # In-Memory Fallback Save
            student_id = str(uuid.uuid4())
            student_data['_id'] = student_id
            self._in_memory_store[student_id] = student_data
            return student_id

        try:
            result = self.collection.insert_one(student_data)
            return str(result.inserted_id)
        except Exception:
            # If insert fails, fall back to memory
            student_id = str(uuid.uuid4())
            student_data['_id'] = student_id
            self._in_memory_store[student_id] = student_data
            return student_id

    def get_student(self, student_id):
        """
        Retrieves a student profile document by ID.
        Searches MongoDB first, then checks in-memory fallback store.
        """
        if not self.is_db_connected():
            return self._in_memory_store.get(str(student_id))

        try:
            # Try ObjectId first
            if ObjectId.is_valid(student_id):
                doc = self.collection.find_one({"_id": ObjectId(student_id)})
                if doc:
                    doc['_id'] = str(doc['_id'])
                    return doc
            
            # Try string match
            doc = self.collection.find_one({"_id": student_id})
            if doc:
                doc['_id'] = str(doc['_id'])
                return doc
            
            # Check fallback store if not in DB
            return self._in_memory_store.get(str(student_id))
        except Exception:
            return self._in_memory_store.get(str(student_id))

    def update_student(self, student_id, updated_data):
        """Updates an existing student document."""
        updated_data['updated_at'] = datetime.now(timezone.utc).isoformat()

        if not self.is_db_connected():
            if str(student_id) in self._in_memory_store:
                self._in_memory_store[str(student_id)].update(updated_data)
                return True
            return False

        try:
            query = {"_id": ObjectId(student_id)} if ObjectId.is_valid(student_id) else {"_id": student_id}
            result = self.collection.update_one(query, {"$set": updated_data})
            if result.matched_count > 0:
                return True
            
            # Check in-memory store
            if str(student_id) in self._in_memory_store:
                self._in_memory_store[str(student_id)].update(updated_data)
                return True
            return False
        except Exception:
            if str(student_id) in self._in_memory_store:
                self._in_memory_store[str(student_id)].update(updated_data)
                return True
            return False

    def list_students(self, limit=10):
        """Lists recent student profiles."""
        if not self.is_db_connected():
            students = list(self._in_memory_store.values())
            return sorted(students, key=lambda x: x.get('updated_at', ''), reverse=True)[:limit]

        try:
            docs = list(self.collection.find().sort("updated_at", -1).limit(limit))
            for doc in docs:
                doc['_id'] = str(doc['_id'])
            return docs
        except Exception:
            students = list(self._in_memory_store.values())
            return sorted(students, key=lambda x: x.get('updated_at', ''), reverse=True)[:limit]
