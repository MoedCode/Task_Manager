# now implement  search.ejs



if  you

this is a search request and  result in case of matches result
API Endpoints

API Endpoint URL: GET http://127.0.0.1:5000/api/search/

Response Body:
```json
{
    "results": [
        {
            "id": "5f6798cb-32b7-48b0-a50b-9a88cd845e23",
            "kickoff": "2025-01-01 03:05:00",
            "priority": "1",
            "task": "مسي علي فخادك",
            "user_id": "f355aeb1-b656-4a02-927a-898b9119a4fc",
            "Task Add Time": "2024-12-02T03:05:30.030629"
        }
    ]
}
```
Request Headers
```json
{
    "Authorization": "Bearer 424e8f4da4b6bcb42153242829588b1490b88b568ad0f55cf5d32a5022b58cb0"
}
```
Request Body
```json
{
"category":"tasks",
"method":"startwith",
"query":{
    "task":"مسي",
    "user_id":"f355aeb1-b656-4a02-927a-898b9119a4fc"
    }
}
```
## example of not matches result
```json
{
    "error": "[False, {'Message': 'No matching rows found.'}]"
}
```
Request Headers (optional):
```json
{
    "Authorization": "Bearer 424e8f4da4b6bcb42153242829588b1490b88b568ad0f55cf5d32a5022b58cb0"
}
```
Request Body (for POST requests):

```json
{
"category":"tasks",
"method":"startwith",
"query":{
    "task":"حالك",
    "user_id":"f355aeb1-b656-4a02-927a-898b9119a4fc"
    }
}
```
so first drop down listn for  `category ` for now  it just tasks may be i add other later
so second  drop down list for   `method  ` which have choices `"startwith", "include", "identical"`
the third  should depends on `category ` if it `tasks` it  will be for task attribute
also input type should depend on attribute  type ..if it date time .. i want date time input
so user can search with just year or month or  day or full date
examples
```json
{
    "results": [
        {
            "id": "1e17dfa9-9f3f-4543-b234-ccef233d0bb1",
            "kickoff": "2024-12-25T03:05",
            "priority": "5",
            "task": "___TASK__ءء",
            "user_id": "f355aeb1-b656-4a02-927a-898b9119a4fc",
            "Task Add Time": "2024-12-02T03:05:43.828982"
        },
        {
            "id": "398a7ba3-9426-4afd-a410-aed82464dca2",
            "kickoff": "2024-12-02 05:05:00",
            "priority": "2",
            "task": "___TASK__2",
            "user_id": "f355aeb1-b656-4a02-927a-898b9119a4fc",
            "Task Add Time": "2024-12-02T03:06:06.210003"
        },
        {
            "id": "ae1ace5b-0ab4-4d5b-a145-39259672966b",
            "kickoff": "2024-12-17 03:07:00",
            "priority": "55",
            "task": "sadsadasd",
            "user_id": "f355aeb1-b656-4a02-927a-898b9119a4fc",
            "Task Add Time": "2024-12-02T03:07:31.901668"
        },
        {
            "id": "06cab49d-419a-4e91-b304-9cb5e831c20b",
            "kickoff": "2024-12-04 03:07:00",
            "priority": "1",
            "task": "sadsadasd",
            "user_id": "f355aeb1-b656-4a02-927a-898b9119a4fc",
            "Task Add Time": "2024-12-02T03:07:41.098814"
        },
        {
            "id": "20e722a2-d0a9-49e4-8677-bc269739961f",
            "kickoff": "2024-12-06 03:12:00",
            "priority": "1",
            "task": "روق علي حالك ",
            "user_id": "f355aeb1-b656-4a02-927a-898b9119a4fc",
            "Task Add Time": "2024-12-02T03:12:13.378254"
        },
        {
            "id": "44511679-6740-4bad-a790-82354efca636",
            "kickoff": "2024-12-13 03:12:00",
            "priority": "1",
            "task": "كله رايح ",
            "user_id": "f355aeb1-b656-4a02-927a-898b9119a4fc",
            "Task Add Time": "2024-12-02T03:12:40.633897"
        }
    ]
}
Request Headers (optional):
{
    "Authorization": "Bearer 424e8f4da4b6bcb42153242829588b1490b88b568ad0f55cf5d32a5022b58cb0"
}
Request Body (for POST requests):
{
"category":"tasks",
"method":"include",
"query":{
    "kickoff":"2024",
    "user_id":"f355aeb1-b656-4a02-927a-898b9119a4fc"
    }
}

```
other one
```json
{
    "results": [
        {
            "id": "5f6798cb-32b7-48b0-a50b-9a88cd845e23",
            "kickoff": "2025-01-01 03:05:00",
            "priority": "1",
            "task": "مسي علي فخادك",
            "user_id": "f355aeb1-b656-4a02-927a-898b9119a4fc",
            "Task Add Time": "2024-12-02T03:05:30.030629"
        }
    ]
}
Request Headers (optional):
{
    "Authorization": "Bearer 424e8f4da4b6bcb42153242829588b1490b88b568ad0f55cf5d32a5022b58cb0"
}
Request Body (for POST requests):
{
"category":"tasks",
"method":"include",
"query":{
    "kickoff":"2025-01-01 03:05:00",
    "user_id":"f355aeb1-b656-4a02-927a-898b9119a4fc"
    }
}

```
other one
```json
{
    "results": [
        {
            "id": "5f6798cb-32b7-48b0-a50b-9a88cd845e23",
            "kickoff": "2025-01-01 03:05:00",
            "priority": "1",
            "task": "مسي علي فخادك",
            "user_id": "f355aeb1-b656-4a02-927a-898b9119a4fc",
            "Task Add Time": "2024-12-02T03:05:30.030629"
        }
    ]
}
Request Headers (optional):
{
    "Authorization": "Bearer 424e8f4da4b6bcb42153242829588b1490b88b568ad0f55cf5d32a5022b58cb0"
}
Request Body (for POST requests):
{
"category":"tasks",
"method":"include",
"query":{
    "kickoff":"03:05:00",
    "user_id":"f355aeb1-b656-4a02-927a-898b9119a4fc"
    }
}


```
the default http://127.0.0.1:5000/api/search/
or it can be passed searchURL





# issue 2
in running express  sever logging output
```sh
::ffff:127.0.0.1 - - [04/Dec/2024:12:43:24 +0000] "POST /search/forward HTTP/1.1" 400 58 "http://127.0.0.1:5001/search" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
```
in running search.ejs clint side output in console

```console
xhr.js:195

 POST http://127.0.0.1:5001/search/forward 400 (Bad Request)
(anonymous)	@	xhr.js:195
xhr	@	xhr.js:15
_t	@	dispatchRequest.js:51
value	@	Axios.js:178
(anonymous)	@	Axios.js:40
p	@	axios.min.js:1
(anonymous)	@	axios.min.js:1
(anonymous)	@	axios.min.js:1
p	@	axios.min.js:1
a	@	axios.min.js:1
(anonymous)	@	axios.min.js:1
r	@	axios.min.js:1
(anonymous)	@	Axios.js:63
(anonymous)	@	Axios.js:217
e.<computed>	@	bind.js:5
performSearch	@	search:199
onclick	@	search:148
```
after clicking debug button



Search
Error: Bad Request: Missing targetEndpoint or payload

DEBUG
Request Debug Info
```json
{
  "url": "http://127.0.0.1:5001/search/forward",
  "headers": {
    "Authorization": "Bearer a66ea866388be68f0b5a7bd1c5907eaef22d4b87627bf931ba74e0051a3ea747",
    "Content-Type": "application/json"
  },
  "body": {
    "category": "tasks",
    "method": "identical",
    "query": {
      "task": "fight",
      "user_id": "f355aeb1-b656-4a02-927a-898b9119a4fc"
    }
  }
}
```

you not search throw all the chat cause if you do .. you will find that that