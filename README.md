 application contain ofim used
 python storage engine
# CsvStorage class  file storage which   act like database with  read , write
write_line ,get columns main methods that deal directly with files
and
 other methods like filter get_by add , delete , multi_selections , search
 that use the main  methods ... to add more advanced features  to storage engine
#  python server
 i intentionally didnt use frame work to know how can i handle  request response parse json data
 serve files   i use  `RequestHandler` class with
    ` _set_headers` Set HTTP headers for the response.
    `serve_html`  serve html files that kust use to serve API interface web page
    mostly during to development test also   I didn't use postman on purpose.
    `parse_request_data`  Parse JSON request body ,  Helper to send a JSON response
    `do_GET` that handle get requests
    `do_POST` handle post requests

 .. i  want to get my hand dirty in those stuff .. despite i can use Flask and Django
 and mysql
 # authentication class , Tokens class
 ## Tokens class
 with  methods  `__init__, create, validate_id, validate_exp, validate_all`
 that handles  creating initialize  Token object validate data that used for initialize it
 ## Authentication class
  which use  Tokens class to initialize token objects for each user
  token object also store user id and user token
  that contain
  ***session authentication***
  Authentication class also sue file storage to store session authentication in file auth.py
  after converting token object instance to dictionary

# models
  contain Base class that has attributes like `created,  updated, id `
  also methods like
  `to_dict` convert object to entirely to serializable dictionary
  `to_save`  covert serializable dictionary to be saved like hashing password
  `serializer` clean the  attributes that unsecure to be relived  from saved dictionaries
  Tasks class and `Users, Tasks, Tokens` classes that inherit  from base class
