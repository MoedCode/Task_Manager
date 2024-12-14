i want nodeJS application that do register
login log out
and when user is logged in can view the home page which is  his  tasks
the application must store the token when user logged and if the user have no token , or n case if the nodeJs app received
Error: 401 Unauthorized user forworn to login page
the login page have also register button that forward
user to register page

also there are a header with all application endpoint
```
server url
http://127.0.0.1:5000/

 routes
/api/
/api/hi/
/api/add/
/api/update/"
/api/login/
/api/logout/
/api/selection/
/api/update/
/api/register/
/api/test/
/api/search/
```
```py

      elif path == "/api/register/":
            not_match = [key for key in data.keys() if key not in Users.KEYS]
            if not_match:
                self.send_response_data(
                    {"Error": f"Invalid keys provided: {not_match}"}, status=200
                )
                return

            username_query = users_stor.is_exist("username", data["username"])
            email_query = users_stor.is_exist("email", data["email"])
            if username_query[0] == "Exist":
                self.send_response_data(
                    {"Error": f"User with username {data['username']} already exists"},
                    status=200,
                )
                return
            if email_query[0] == "Exist":
                self.send_response_data(
                    {"Error": f"User with email {data['email']} already exists"},
                    status=200,
                )
                return

            result = Users.create(**data)
            if not result[0]:
                self.send_response_data({"Error": result[1]}, status=422)
                return

            user_dict = result[1].to_save()
            users_stor.add(user_dict)
            users_stor.save()
            log_res = auth.login_user(user_dict)
            if not log_res[0]:
                self.send_response_data({"Error": log_res[1]}, status=400)
                return

            token = log_res[1]
            self.send_response_data(
                {"success": "User registered successfully", "token": token, "user": user_dict},
                status=201,
            )

        else:
            self.send_response_data({"Error": "Endpoint not found"}, status=404)

        elif path == "/api/home/":
            res, user_id = self.get_token_dict()
            if not  res:
                print(f"{DEBUG()} -- {user_id}")
                self.send_response_data({"error": f"Not Found {user_id}"}, status=S401)
                return
            all_tasks = tasks_stor.csv_read()
            user_tasks = []
            for task in all_tasks:
                if task["user_id"] == user_id:
                    user_tasks.append(task)

            self.send_response_data(self.get_user_tasks()[1])
        else:
            self.send_response_data({"error": "Not Found"}, status=404)

        if path == "/api/login/":
            username = data.get("username")
            password = data.get("password")
            if not username or not password:
                self.send_response_data({"Error": "Missing username or password"}, status=400)
                return

            res = auth.authenticate(username=username, password=password)
            if not res[0]:
                self.send_response_data({"Error": res[1]}, status=200)
                return

            login_res = auth.login_user(res[1])
            if not login_res[0]:
                self.send_response_data({"Error": login_res[1]}, status=200)
                return

            self.send_response_data({"status": "success", "token": login_res[1]})

        elif path == "/api/logout/":
            print(f"{path}: self.headers{self.headers}")
            if data and data.get("id"):
                user_id = data.get("id")
                x =  auth.logout(user_id=user_id)
                print(f"{path} : user_id {user_id} x{x}")
                self.send_response_data({"status": "success", "message": f"{self.headers} Logged out"})
                return
            auth_header = self.headers.get("Authorization", "")
            print(f" Error -- {path} : auth_header before : {auth_header} {type(auth_header)}")
            if not auth_header:


                self.send_response_data({"Error": "Missing Authorization header"}, status=400)
                return
            parsed_token = auth_header.split(" ")[1]
            logout_res = auth.delete_token(parsed_token)
            print(f" Error -- {path} : parsed_token : {parsed_token}")
            if logout_res[0]:
                self.send_response_data({"status": "success", "message": "Logged out"})
            else:
                self.send_response_data({"Error": f"Invalid token {logout_res[1]}"}, status=400)


```
```sh
mohamed@DESKTOP-S296B4S /mnt/c/Users/Active/Desktop/Coding/Gradutaion/simple_tasker/frontend
 % sudo npm install axios
npm WARN read-shrinkwrap This version of npm is compatible with lockfileVersion@1, but package-lock.json was generated for lockfileVersion@3. I'll try to do my best with it!
npm WARN deprecated core-js@2.6.12: core-js@<3.23.3 is no longer maintained and not recommended for usage due to the number of issues. Because of the V8 engine whims, feature detection in old core-js versions could cause a slowdown up to 100x even if nothing is polyfilled. Some versions have web compatibility issues. Please, upgrade your dependencies to the actual version of core-js.
npm WARN deprecated urix@0.1.0: Please see https://github.com/lydell/urix#deprecated
npm WARN deprecated source-map-resolve@0.5.3: See https://github.com/lydell/source-map-resolve#deprecated
npm WARN deprecated source-map-url@0.4.1: See https://github.com/lydell/source-map-url#deprecated
npm WARN deprecated resolve-url@0.2.1: https://github.com/lydell/resolve-url#deprecated
npm WARN deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and powerful.
npm WARN deprecated glob@7.0.6: Glob versions prior to v9 are no longer supported
npm WARN deprecated uuid@2.0.3: Please upgrade  to version 7 or higher.  Older versions may use Math.random() in certain circumstances, which is known to be problematic.  See https://v8.dev/blog/math-random for details.
npm WARN deprecated glob@7.2.3: Glob versions prior to v9 are no longer supported

> msgpackr-extract@3.0.3 install /mnt/c/Users/Active/Desktop/node_modules/msgpackr-extract
> node-gyp-build-optional-packages


> core-js@2.6.12 postinstall /mnt/c/Users/Active/Desktop/node_modules/core-js
> node -e "try{require('./postinstall')}catch(e){}"

Thank you for using core-js ( https://github.com/zloirock/core-js ) for polyfilling JavaScript standard library!

The project needs your help! Please consider supporting of core-js on Open Collective or Patreon:
> https://opencollective.com/core-js
> https://www.patreon.com/zloirock

Also, the author of core-js ( https://github.com/zloirock ) is looking for a good job -)

npm WARN optional SKIPPING OPTIONAL DEPENDENCY: @msgpackr-extract/msgpackr-extract-linux-arm64@3.0.3 (node_modules/msgpackr-extract/node_modules/@msgpackr-extract/msgpackr-extract-linux-arm64):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for @msgpackr-extract/msgpackr-extract-linux-arm64@3.0.3: wanted {"os":"linux","arch":"arm64"} (current: {"os":"linux","arch":"x64"})
npm WARN optional SKIPPING OPTIONAL DEPENDENCY: @msgpackr-extract/msgpackr-extract-win32-x64@3.0.3 (node_modules/msgpackr-extract/node_modules/@msgpackr-extract/msgpackr-extract-win32-x64):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for @msgpackr-extract/msgpackr-extract-win32-x64@3.0.3: wanted {"os":"win32","arch":"x64"} (current: {"os":"linux","arch":"x64"})
npm WARN optional SKIPPING OPTIONAL DEPENDENCY: @msgpackr-extract/msgpackr-extract-darwin-x64@3.0.3 (node_modules/msgpackr-extract/node_modules/@msgpackr-extract/msgpackr-extract-darwin-x64):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for @msgpackr-extract/msgpackr-extract-darwin-x64@3.0.3: wanted {"os":"darwin","arch":"x64"} (current: {"os":"linux","arch":"x64"})
npm WARN optional SKIPPING OPTIONAL DEPENDENCY: @msgpackr-extract/msgpackr-extract-darwin-arm64@3.0.3 (node_modules/msgpackr-extract/node_modules/@msgpackr-extract/msgpackr-extract-darwin-arm64):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for @msgpackr-extract/msgpackr-extract-darwin-arm64@3.0.3: wanted {"os":"darwin","arch":"arm64"} (current: {"os":"linux","arch":"x64"})
npm WARN optional SKIPPING OPTIONAL DEPENDENCY: @msgpackr-extract/msgpackr-extract-linux-arm@3.0.3 (node_modules/msgpackr-extract/node_modules/@msgpackr-extract/msgpackr-extract-linux-arm):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for @msgpackr-extract/msgpackr-extract-linux-arm@3.0.3: wanted {"os":"linux","arch":"arm"} (current: {"os":"linux","arch":"x64"})
npm WARN active@1.0.0 No description
npm WARN active@1.0.0 No repository field.

+ axios@1.7.8
added 12 packages from 22 contributors, removed 3 packages, updated 282 packages and audited 305 packages in 159.879s

24 packages are looking for funding
  run `npm fund` for details

found 21 vulnerabilities (7 low, 5 moderate, 9 high)
  run `npm audit fix` to fix them, or `npm audit` for details


   ╭────────────────────────────────────────────────────────────────╮
   │                                                                │
   │      New major version of npm available! 6.14.18 → 10.9.1      │
   │   Changelog: https://github.com/npm/cli/releases/tag/v10.9.1   │
   │               Run npm install -g npm to update!                │
   │                                                                │
   ╰────────────────────────────────────────────────────────────────╯

mohamed@DESKTOP-S296B4S /mnt/c/Users/Active/Desktop/Coding/Gradutaion/simple_tasker/frontend
```