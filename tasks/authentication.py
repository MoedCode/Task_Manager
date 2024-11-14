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
    def authenticate(self, user={}):
        pass
    def is_login(self, user={}):
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




    def login(self, user={}):
        # if not isinstance(user, Users):
        if user["class_name"] != "Users":
            return False, f"user must be {Users} instance"
        query=users_stor.get_by(key="username", value=user["username"])
        if not query[0]:
            return False, f"user is not registered . \n {query[1]} "
        result = Tokens.create(user_id=query[1]["id"])

        if  not result[0]:
            return False, f"{self.__class__.__name__}.login()\n {result[1]} "
        exi_res = tokens_stor.is_exist("user_id", query[1]["id"])
        # if not exi_res[]
        print(f"exi_res :: {exi_res}")
        if exi_res[0] == "Exist":
            return False, f"user {query[1]['username']} is already logged in"
        token_dict = result[1].to_save()
        adding = tokens_stor.add(token_dict)
        saving = tokens_stor.save()

        if not saving or not adding:
            return saving if not saving else adding
        return True , result[1].hash_token

if __name__  == "__main__":
    auth = Authentication()
    query =  users_stor.get_by("username", "alsamurai")
    # print(auth.authenticate({})query = users_stor.get_by("username", "alsamurai")

    print(f"user : {query[1]}")
    print(f"auth.login(user): {auth.login(query[1])}")
    print(f"auth.is_login(user): {auth.is_login(query[1])}")