import re
import uuid
from datetime import datetime,  timedelta
import hashlib
import time
import bcrypt
# Create your models here.
class Base:
    immutable_instattr = ["created", "id","class_name", "password" ]
    def __init__(self):
        self.id = uuid.uuid4()
        self.created = datetime.now()
        self.updated = datetime.now()
        self.time_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.class_name = self.__class__.__name__
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
        temp = self.to_dict()
        if "time_format" in temp:
            temp.pop("time_format")
        if "password" in temp:
            # Hash the password using SHA-256 to match `check_PWD_256`
            temp["password"] = hashlib.sha256(temp["password"].encode('utf-8')).hexdigest()
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
    KEYS = ["class_name","task", "priority", "kickoff", "id", "user_id", "created", "updated"]
    def __init__(self, task, priority, kickoff, user_id):
        super().__init__()
        self.task = task
        self.priority = priority
        self.user_id = user_id
        # Use fromisoformat to handle the datetime string
        self.kickoff = datetime.fromisoformat(kickoff)


    def __repr__(self):
        return (f"Tasks(task='{self.task}', priority={self.priority}, kickoff='{self.kickoff}', "
                f"id='{self.id}', user_id='{self.user_id}', created='{self.created}', updated='{self.updated}')")


class Users(Base):
    KEYS = ["class_name","username","email","password","image", "id", "created", "updated"]

    # Using a private __init__ to prevent direct instantiation
    def __init__(self, username, email, password, image=None):
        super().__init__()
        self.username = username
        self.email = email
        self.password = password
        self.image = image


    @classmethod
    def create(cls, username, email, password, image=None):
        """
        Factory method to validate all fields and return a Users instance if valid.
        Raises a ValueError if validation fails.
        """
        instance = cls.__new__(cls)  # Create an uninitialized instance
        is_valid, result = instance.validate_all(username, email, password, image)
        if is_valid:
            # Initialize the instance with validated data
            instance.__init__(username=result['username'],
                              email=result['email'],
                              password=result['password'],
                              image=result.get('image'))
            return True , instance
        else:
            # Raise an error with all validation issues
            return False,  "Validation errors: " + "; ".join(result)

    def valid_username(self, value):
        """Validates the username"""
        if len(value) < 5:
            return False, "Username must be at least 5 characters long."
        if not value.isalnum():
            return False, "Username must contain only letters and numbers."
        return True, value

    def valid_email(self, value):
        """Validates the email format"""
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, value):
            return False, "Invalid email format."
        return True, value

    def valid_password(self, value):
        """Validates the password strength"""
        if len(value) < 8:
            return False, "Password must be at least 8 characters long."
        if not any(char.isdigit() for char in value):
            return False, "Password must contain at least one number."
        if not any(char.isalpha() for char in value):
            return False, "Password must contain at least one letter."
        return True, value

    def valid_image(self, value):
        """Validates the image (optional)"""
        if value and not value.lower().endswith(('jpg', 'jpeg', 'png')):
            return False, "Image must be in JPG, JPEG, or PNG format."
        return True, value

    def validate_all(self, username, email, password, image=None):
        """Validate all attributes and return validation status"""
        error_messages = []
        clean_data = {}

        # Validate each attribute, collecting results and errors
        username_valid, username = self.valid_username(username)
        if username_valid:
            clean_data['username'] = username
        else:
            error_messages.append(username)

        email_valid, email = self.valid_email(email)
        if email_valid:
            clean_data['email'] = email
        else:
            error_messages.append(email)

        password_valid, password = self.valid_password(password)
        if password_valid:
            clean_data['password'] = password
        else:
            error_messages.append(password)

        image_valid, image = self.valid_image(image)
        if image_valid or image is None:
            clean_data['image'] = image
        else:
            error_messages.append(image)

        # Return validation status and data or errors
        if error_messages:
            return False, error_messages
        return True, clean_data

    @classmethod
    def validate_dict(cls, data={}, instance=None):
        """
        Dynamically validates user attributes provided in `data`.
        Can be called as both an instance method and a class method.
        Returns:
            - True, clean_data (if all attributes are valid)
            - False, error_messages (if any attribute fails validation)
        """
        error_messages = {}
        clean_data = {}

        # Use instance methods if called from an instance
        if instance:
            validation_methods = {
                "username": instance.valid_username,
                "email": instance.valid_email,
                "password": instance.valid_password,
                "image": instance.valid_image
            }
        else:
            # Use class methods for validation
            validation_methods = {
                "username": cls.valid_username,
                "email": cls.valid_email,
                "password": cls.valid_password,
                "image": cls.valid_image
            }

        # Iterate through provided data and validate each key-value pair
        for key, value in data.items():
            if key in validation_methods:
                is_valid, result = validation_methods[key](cls, value) if not instance else validation_methods[key](value)
                if is_valid:
                    clean_data[key] = result
                else:
                    error_messages[key] = result
            else:
                error_messages[key] = f"Validation for '{key}' is not supported."

        # Return results
        if error_messages:
            return False, error_messages
        return True, clean_data
    def __str__(self) -> str:
        return self.username


class Tokens(Base):
    KEYS = ["class_name","id" ,"user_id", "created", "token", "token_time"]
    def __init__(self, user_id=None, token_time=21600 ):
        super().__init__()
        if hasattr(self, 'updated'):
            del self.updated
        # if hasattr(self, 'id'):
        #     del self.id
        """
        Initializes the TokenManager with an optional token expiration time.
        :param token_expiry: Token expiration time in seconds (default: 1 hour)
        """
        raw_token = f"{user_id}-{time.time()}"
        self.token = hashlib.sha256(raw_token.encode()).hexdigest()
        self.token_time = token_time  # Expiry time for tokens in seconds
        self.user_id = user_id
    @classmethod
    def create(cls, user_id=None, token_time=86400 ):
        instance = cls.__new__(cls)
        result = instance.validate_all(user_id, token_time )
        if not result[0]:
            return False, result[1]

        instance.__init__(**result[1])

        return True, instance

    def validate_id(self, user_id):
        if isinstance(user_id, str):
            try:
                uuid.UUID(user_id).version == 4
                return True, user_id , "str"
            except Exception as e:
                    return False, str(e) + " not match valid UUID format V4 "
        try:
            user_id.version == 4
            return True, str(user_id), "obj"
        except Exception as e:
            return False, str(e) + " not match valid UUID format V4 "
    def validate_exp(self, token_time):
        try:
            exp_time_int = int(token_time)
            if 21600 <= exp_time_int <= 172800:  # Check if within range
                return True, exp_time_int
            else:
                # Return False with message if out of range
                return False, "Expiration time must be between 21600 and 172800 seconds."
        except ValueError:
            msg = "Expiration time should be an integer within the range 21600-172800."
            return False, msg
    def validate_all(self, user_id=None, token_time=None ):
        id_result = self.validate_id(user_id)
        exp_result = self.validate_exp(token_time)
        errors_messages = ""
        clean_data = {}
        if  id_result[0]:
            clean_data["user_id"] = id_result[1]
        else:
            errors_messages += f" -{id_result[1]}\n"
        if exp_result[0]:
            clean_data["token_time"] = exp_result[1]
        else:
            errors_messages= f"-{exp_result[1]}\n"
        if errors_messages:
            return False, errors_messages
        return True, clean_data

if __name__ == "__main__":
    user = Users.create("johziko", "john@example.com", "securePassword123", "profile.jpg")
    user = Users(username="john_doe", email="john@example.com", password="securePass1")

    # Example of validating all attributes
    data_to_validate = {
        "username": "newuser",
        "email": "new_user@example.com",
        # "password": "NewPass123",
        # "image": "profile.png"
    }
    result = user.validate_dict(data_to_validate)

    print( result)

