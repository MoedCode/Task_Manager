# from models import *
from tasks.__init__ import *

class Authentication:
    def request_MD(request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        content_type = request.META.get('CONTENT_TYPE', '')

        # Alternatively, to get all headers as a dictionary
        headers = {key: value for key, value in request.META.items() if key.startswith('HTTP_')}
        x = {
            'auth_header': auth_header, 'content_type': content_type,
            "headers":headers
        }
        return  x
    def token_remaining_time(self, created, token_time):
        token_time = int(token_time)
        # Parse the created time string to a datetime object
        created_time = datetime.strptime(created, '%Y-%m-%dT%H:%M:%S.%f')

        # Calculate expiry time by adding validity period to the created time
        expiry_time = created_time + timedelta(seconds=token_time)

        # Calculate remaining time by subtracting the current time from expiry time
        time_left = expiry_time - datetime.now()

        # If time_left is positive, return remaining time in seconds; otherwise, return 0
        return max(time_left.total_seconds(), 0)
    def validate_token(self, token=""):
        if not token:
            return False, f"Error {self.validate_token}: No valid token provided"
        if token.startswith("Token") or token.startswith("Bearer"):
            token = token.split(" ")[1]
        query = tokens_stor.get_by("token", token)
        if not query[0]:
            return query
        token_dict = query[1]
        remaining = self.token_remaining_time(created=token_dict["created"], token_time=token_dict["token_time"])
        if remaining < 60:
            tokens_stor.delete("token", token)
            return False, "Your session has expired. Please log in again."
        return True, token_dict
        pass
    def authenticate(self, user={}):
        pass
    def is_login(self,  request={}):

        req_token = request.headers.get('Authorization') or None
        if not request or not req_token:
            return False , f"No valid token {req_token}"
        token_query = tokens_stor.is_exist("token",req_token)
        if not token_query[0] or token_query[0] == "Not Exist":
            return False, "Not logged in "
        if token_query[0] == "Exist":
            token =token_query[1]
            rem_time = self.token_remaining_time(created=token["created"],token_time=token["token_time"])
            if int(rem_time) > 60:
                return True , f"gooood {rem_time}"
            else:
                res_x = tokens_stor.delete("token", token["token"])
                return False, "5lalas ra7et 3alek"
    def authenticate(self, username=None, password=None):

        query = users_stor.get_by("username", username)
        if not query[0]:
            return False, query[1]
        validPWD = self.check_PWD_256(plain_password=password, hashed_password=query[1]["password"])
        if not query[0] or  not validPWD:
            if not validPWD:
                return False,  f"Query {query[1]} hashpass {self.hash_256(password)}"
            return  (False, f"incorrect username or password ")
        return True, query[1]

    def hash_256(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_PWD_256(self, plain_password, hashed_password):
        return self.hash_256(plain_password) == hashed_password

    def is_login_1(self, user={}):

        if not user or not  user["id"]:
            return False, f"No valid user data "
        token_query = tokens_stor.is_exist("user_id",user["id"])
        if not token_query[0] or token_query[0] == "Not Exist":
            return False, "Not logged in "
        if token_query[0] == "Exist":
            token =token_query[1]
            rem_time = self.token_remaining_time(created=token["created"],token_time=token["token_time"])
            if int(rem_time) > 60:
                return True , f"gooood {rem_time}"
            else:
                res_x = tokens_stor.delete("token", token["token"])
                return False, "5lalas ra7et 3alek"


    def delete_token(self, user_token=None):
        if not user_token:
            False, f"Auth Error {self.logout.__name__}: NULL user token"
        # okay, query = tokens_stor.get_by("token", user_token)
        # if not okay:
        #     return False, query
        okay, delres = tokens_stor.delete("token", user_token)
        if not okay:
            return False, delres
        return  True, delres
    def logout(self, user={}):
        if not user:
            return False, f"Error -- {self.logout}: NULL user and user id"
        key = list(user.keys())[0]
        value = user[key]
        query_user = users_stor.filter({key:value}, True)
        if not query_user["id"]:
            return False, f"Error {key} : {value}"
        user_id = query_user["id"]
        okay, query = tokens_stor.delete("user_id",  user_id)
        if not okay:
            return False, query
        return True, f"user with {key}:{value}  logged out"


    def update_user(self, user={},data={}):
        if not user or not data :
            return False , "5od pa3dak we amshe  ala"

        username = user["username"] or None
        password = user["password"] or None
        if not username or not password:
            return False, f"No {'password' if not password else ''} {'username' if not username else ''}"

        query = users_stor.get_by(key="username", value=username)
        if not query[0]:
            return False, "no valid credential 1"
        valid_PWD = self.check_PWD_256(plain_password=password, hashed_password=query[1]["password"])
        if not valid_PWD:
            return  False, "no valid credential 2"
        idx = query[2]
        clean_data = Users.validate_dict(data=data)
        if not clean_data[0]:
            return clean_data
        if "password" in clean_data[1]:
            clean_data[1]["password"]= self.hash_256(clean_data[1]["password"])
        self.logout(user=query[1])
        for key, value in clean_data[1].items():
            users_stor.session[idx][key] = value
            users_stor.save()
        return True, clean_data[1]

    def is_auth(self, headers={}, token=""):
        if not token and not headers:
            return False, "No valid token or headers"
        if not token :
            token = headers.get("Authorization", "")
        query = self.validate_token(token)
        if not query[0]:
            return False,  f" {query[1]}"
        return True, query[1]
    def get_user(self, headers:dict={}, token:str="") ->List[Dict]:
        """ check if user authenticated , if so return token , user dict
            it require headers or token using self.is_auth
            Args:
                headers (dict): which is request headers
                token (str): can path token directly then no headers needed
                Return:
                        list of True , token dictionary, user dictionary,
                        on error returns list of False a appropriate error message
        """
        auth_res = self.is_auth(headers, token)
        if not  auth_res[0]:
            return list(auth_res)
        user_id = auth_res[1]["user_id"]
        user_query = users_stor.filter({"id":user_id}, True)
        return [True, auth_res[1],user_query ]

    def login_user(self, user={}):
        # if not isinstance(user, Users):
        if user["class_name"] != "Users":
            return False, f"user must be {Users} instance"
        query=users_stor.get_by(key="username", value=user["username"])
        if not query[0]:
            return False, f"user is not registered . \n {query[1]} "
        result = Tokens.create(user_id=query[1]["id"])

        if  not result[0]:
            return False, f"{self.__class__.__name__}.login()\n {result[1]} "
        exi_res = tokens_stor.get_by("user_id", query[1]["id"])


        if exi_res[0]:
            idx = exi_res[2]
            tokens_stor.session.pop(idx)
            tokens_stor.save()
        token_dict = result[1].to_save()
        adding = tokens_stor.add(token_dict)
        saving = tokens_stor.save()

        # if not saving or not adding:
            # return saving if not saving else adding
        return True , result[1].token

if __name__  == "__main__":
    auth = Authentication()
    # query =  users_stor.get_by("username", "alsamurai")
    # print(auth.authenticate({})query = users_stor.get_by("username", "alsamurai")

    # print(f"user : {query[1]}")
    # print(f"auth.login(user): {auth.login(query[1])}")
    # print(f"auth.is_login(user): {auth.is_login(query[1])}")
    # user = Users.create(username="john_doe", email="john@example.com", password="securePass1")

    # Example of validating all attributes
    data_to_validate = {
        "username": "prowuser",
        "email": "new_user@example.com",
        "image": "profile.png",
    }
    DEBUG(f'{users_stor.write_line({"username":"newuser"}, data_to_validate, True)}')
    # print(f'{users_stor.filter({"username":"procodexx1"},True )}')
    ProCoderx0 = {"username":"ProCoderx0", "password":"ProCoderx0"}
    # x = auth.update_user(user=ProCoderx0, data=data_to_validate)
    # print(x)