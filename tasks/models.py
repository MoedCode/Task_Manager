import uuid
from datetime import datetime

import bcrypt
# Create your models here.
class Base:
    def __init__(self):
        self.id = uuid.uuid4()
        self.created = datetime.now()
        self.updated = datetime.now()
        self.time_format = "%Y-%m-%dT%H:%M:%S.%f"
    def to_dict(self):
        new_dict = self.__dict__.copy()
        new_dict['id'] = str(new_dict['id'])
        if "created" in new_dict:
            new_dict['created'] = new_dict['created'].strftime(self.time_format)
        if "updated" in new_dict:
            new_dict['updated'] = new_dict['updated'].strftime(self.time_format)
        new_dict.pop('_state', None)
        if 'date_joined' in new_dict:
            new_dict['date_joined'] = new_dict['date_joined'].strftime(self.time_format)

        if 'user_id' in new_dict:
            new_dict['user_id'] = str(new_dict['user_id'])
        return new_dict
    def to_save(self):
        salt = bcrypt.gensalt()
        temp = self.to_dict()
        if "time_format" in temp:
            temp.pop("time_format")
        if "password" in temp:
            temp["password"] =  bcrypt.hashpw(temp["password"], salt)
        return temp
    def serializer(self):
        serialized = self.to_dict()
        if 'password' in serialized:
            serialized.pop("password")
        if 'created' in serialized:
            serialized.pop("created")
        if 'updated' in serialized:
            serialized.pop("updated")
        return serialized
class Tasks(Base):
    def __init__(self, task, priority, kickoff, username):
        super().__init__()
        self.task = task
        self.priority = priority
        self.username = username
        # Use fromisoformat to handle the datetime string
        self.kickoff = datetime.fromisoformat(kickoff)

    def __repr__(self):
        return (f"Tasks(task='{self.task}', priority={self.priority}, kickoff='{self.kickoff}', "
                f"id='{self.id}', username='{self.username}', created='{self.created}', updated='{self.updated}')")

class Users(Base):
    pass