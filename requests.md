# Python `requests` Module — Complete Guide

## 1. What is the `requests` module?

`requests` is a Python third-party library used to make **HTTP requests** to web servers and APIs.

It allows Python to communicate with:

* REST APIs
* Django APIs
* DRF APIs
* websites
* authentication endpoints
* external services

For example:

```python
import requests

response = requests.get("https://example.com")

print(response.status_code)
print(response.text)
```

The basic idea is:

```text
Python program
      |
      | HTTP request
      ↓
Web server / API
      |
      | HTTP response
      ↓
Python program
```

---

# 2. Installing `requests`

`requests` does not normally come with Python.

Install it with:

```bash
pip install requests
```

Check:

```bash
pip show requests
```

Or:

```bash
python -m pip show requests
```

Then:

```python
import requests
```

---

# 3. HTTP methods

The most important HTTP methods are:

```text
GET       → retrieve data
POST      → create/send data
PUT       → replace/update data
PATCH     → partially update data
DELETE    → delete data
```

With `requests`, they correspond to:

```python
requests.get()
requests.post()
requests.put()
requests.patch()
requests.delete()
```

---

# 4. GET request

A GET request retrieves data.

```python
import requests

response = requests.get(
    "https://example.com"
)

print(response)
print(response.status_code)
print(response.text)
```

A response may look like:

```text
<Response [200]>
```

`200` means the request was successful.

---

# 5. Understanding `response`

When you do:

```python
response = requests.get(url)
```

`response` is a `requests.Response` object.

It contains information returned by the server.

Important properties and methods include:

```python
response.status_code
response.text
response.content
response.json()
response.headers
response.url
response.cookies
response.reason
response.ok
```

---

# 6. `status_code`

```python
print(response.status_code)
```

Example:

```text
200
```

Common HTTP status codes:

```text
200 → OK
201 → Created
204 → No Content

301 → Permanent redirect
302 → Temporary redirect

400 → Bad Request
401 → Unauthorized
403 → Forbidden
404 → Not Found
405 → Method Not Allowed

500 → Internal Server Error
502 → Bad Gateway
503 → Service Unavailable
```

Example:

```python
if response.status_code == 200:
    print("Request successful")
```

---

# 7. `response.text`

`text` gives the response body as a string.

```python
response = requests.get("https://example.com")

print(response.text)
```

For an HTML page, you might receive:

```html
<!DOCTYPE html>
<html>
...
</html>
```

For an API, the response may be JSON represented as text:

```text
{"name": "Laptop", "price": 500}
```

---

# 8. `response.json()`

When the server returns JSON, use:

```python
data = response.json()
```

Example:

```python
import requests

response = requests.get(
    "https://api.example.com/products/"
)

data = response.json()

print(data)
```

If the API returns:

```json
{
    "name": "Laptop",
    "price": 500
}
```

then Python converts it into a dictionary:

```python
{
    "name": "Laptop",
    "price": 500
}
```

You can then do:

```python
print(data["name"])
print(data["price"])
```

---

# 9. `response.content`

`content` gives the response body as bytes.

```python
print(response.content)
```

This is useful for binary data such as:

* images
* PDFs
* ZIP files
* other files

Example:

```python
response = requests.get(image_url)

with open("image.jpg", "wb") as file:
    file.write(response.content)
```

---

# 10. `response.headers`

HTTP responses contain headers.

```python
print(response.headers)
```

You can retrieve a particular header:

```python
print(response.headers["Content-Type"])
```

Or:

```python
print(response.headers.get("Content-Type"))
```

Example:

```text
application/json
```

Using `.get()` is safer if the header might not exist.

---

# 11. `response.url`

Shows the final URL.

```python
print(response.url)
```

Useful when redirects occur.

---

# 12. `response.ok`

`ok` tells you whether the response is generally considered successful.

```python
if response.ok:
    print("Success")
else:
    print("Request failed")
```

It is roughly:

```text
status code < 400 → True
status code >= 400 → False
```

For detailed API handling, checking the exact status code is often better.

---

# 13. `response.reason`

```python
print(response.reason)
```

Example:

```text
OK
```

or:

```text
Not Found
```

---

# 14. Query parameters

Suppose you want:

```text
/products/?name=laptop
```

You can manually write:

```python
requests.get(
    "http://127.0.0.1:8000/products/?name=laptop"
)
```

But `requests` provides a better way.

Use `params`:

```python
params = {
    "name": "laptop"
}

response = requests.get(
    "http://127.0.0.1:8000/products/",
    params=params
)
```

Requests constructs:

```text
/products/?name=laptop
```

---

# 15. Multiple query parameters

```python
params = {
    "name": "laptop",
    "min_price": 100,
    "max_price": 1000
}

response = requests.get(
    "http://127.0.0.1:8000/products/",
    params=params
)
```

The resulting URL is approximately:

```text
/products/?name=laptop&min_price=100&max_price=1000
```

Check it:

```python
print(response.url)
```

---

# 16. POST request

POST is commonly used to create data.

```python
data = {
    "name": "Laptop",
    "price": 500
}

response = requests.post(
    "http://127.0.0.1:8000/products/",
    data=data
)
```

---

# 17. Sending JSON

For REST APIs, you will frequently use:

```python
json=data
```

Example:

```python
data = {
    "name": "Laptop",
    "price": 500,
    "stock": 10
}

response = requests.post(
    "http://127.0.0.1:8000/api/products/",
    json=data
)
```

This is different from:

```python
data=data
```

### `json=`

```python
requests.post(url, json=data)
```

automatically sends JSON.

The request will have an appropriate content type such as:

```text
Content-Type: application/json
```

For REST APIs, `json=` is usually what you want when the endpoint expects JSON.

---

# 18. `data=` vs `json=`

This distinction is important.

### `data=`

```python
requests.post(
    url,
    data={
        "username": "nzegge",
        "password": "12345678"
    }
)
```

Used for form-style data.

### `json=`

```python
requests.post(
    url,
    json={
        "username": "nzegge",
        "password": "12345678"
    }
)
```

Used for JSON APIs.

Think:

```text
data= → form/request body data
json=  → JSON request body
```

---

# 19. Headers

HTTP headers provide additional information about the request.

Use:

```python
headers = {
    "Content-Type": "application/json"
}

response = requests.post(
    url,
    json=data,
    headers=headers
)
```

For many JSON requests, `requests` handles the JSON content type automatically when using `json=`.

---

# 20. Authorization headers

This is particularly important with your Django REST API.

Suppose your API uses JWT authentication.

You may have:

```text
Authorization: Bearer <access_token>
```

In Python:

```python
headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(
    "http://127.0.0.1:8000/api/orders/",
    headers=headers
)
```

The server receives:

```text
Authorization: Bearer eyJ...
```

---

# 21. JWT login with Requests

Suppose your Django SimpleJWT endpoint is:

```text
/api/token/
```

You can do:

```python
import requests

data = {
    "username": "nzegge",
    "password": "12345678"
}

response = requests.post(
    "http://127.0.0.1:8000/api/token/",
    json=data
)

print(response.status_code)
print(response.json())
```

A successful response might contain:

```json
{
    "refresh": "...",
    "access": "..."
}
```

Get the access token:

```python
tokens = response.json()

access_token = tokens["access"]

print(access_token)
```

---

# 22. Use JWT token

Then:

```python
headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(
    "http://127.0.0.1:8000/api/orders/",
    headers=headers
)

print(response.status_code)
print(response.json())
```

The complete flow:

```text
Login
  ↓
POST /api/token/
  ↓
Receive access token
  ↓
Put token in Authorization header
  ↓
GET /api/orders/
```

---

# 23. PUT request

PUT generally replaces an existing resource.

```python
data = {
    "name": "Updated Laptop",
    "price": 700,
    "stock": 20
}

response = requests.put(
    "http://127.0.0.1:8000/api/products/1/",
    json=data
)
```

---

# 24. PATCH request

PATCH is generally used for a partial update.

For example, change only the price:

```python
data = {
    "price": 750
}

response = requests.patch(
    "http://127.0.0.1:8000/api/products/1/",
    json=data
)
```

You don't necessarily need to send every field.

---

# 25. DELETE request

```python
response = requests.delete(
    "http://127.0.0.1:8000/api/products/1/"
)

print(response.status_code)
```

A successful DELETE often returns:

```text
204
```

There may be no response body.

Therefore, don't automatically do:

```python
response.json()
```

after every DELETE.

---

# 26. Timeout

Always consider using a timeout when making requests to external services.

```python
response = requests.get(
    url,
    timeout=10
)
```

This means Requests will not wait indefinitely.

You can also specify separate timeouts:

```python
response = requests.get(
    url,
    timeout=(5, 30)
)
```

Meaning:

```text
5 seconds  → connection timeout
30 seconds → read timeout
```

---

# 27. Handling exceptions

Requests provides exceptions.

```python
import requests

try:
    response = requests.get(
        "https://example.com",
        timeout=10
    )

except requests.RequestException as error:
    print("Request failed:", error)
```

`RequestException` is a general Requests exception.

---

# 28. `raise_for_status()`

This is extremely useful.

```python
response = requests.get(url)

response.raise_for_status()
```

If the response is successful, execution continues.

If the server returns an HTTP error such as:

```text
404
500
```

Requests raises an exception.

Example:

```python
try:
    response = requests.get(
        "https://example.com",
        timeout=10
    )

    response.raise_for_status()

    print(response.json())

except requests.RequestException as error:
    print("Request failed:", error)
```

---

# 29. Checking status manually

You can also do:

```python
if response.status_code == 200:
    print("Success")

elif response.status_code == 404:
    print("Not found")

elif response.status_code == 500:
    print("Server error")
```

This is useful when you need different behavior for specific status codes.

---

# 30. Cookies

You can access cookies:

```python
response.cookies
```

For example:

```python
for cookie in response.cookies:
    print(cookie.name, cookie.value)
```

You can also send cookies:

```python
cookies = {
    "sessionid": "abc123"
}

response = requests.get(
    url,
    cookies=cookies
)
```

---

# 31. Sessions

A `Session` allows you to maintain information between requests.

```python
session = requests.Session()
```

Then:

```python
session.get(url)
session.post(url)
session.get(url)
```

A session can maintain things such as:

* cookies
* headers
* authentication-related state
* connection pooling

Example:

```python
import requests

session = requests.Session()

session.headers.update({
    "User-Agent": "My Python App"
})

response = session.get(
    "https://example.com"
)
```

---

# 32. Session with JWT

You can put your authorization header into a session:

```python
session = requests.Session()

session.headers.update({
    "Authorization": f"Bearer {access_token}"
})
```

Now:

```python
response = session.get(
    "http://127.0.0.1:8000/api/orders/"
)
```

and:

```python
response = session.get(
    "http://127.0.0.1:8000/api/products/"
)
```

automatically use the Authorization header.

Instead of repeatedly doing:

```python
headers=headers
```

---

# 33. File upload

Requests can upload files.

```python
files = {
    "image": open("product.jpg", "rb")
}

response = requests.post(
    "http://127.0.0.1:8000/api/products/",
    files=files
)
```

Better:

```python
with open("product.jpg", "rb") as file:

    files = {
        "image": file
    }

    response = requests.post(
        "http://127.0.0.1:8000/api/products/",
        files=files
    )
```

This is useful when your Django model contains:

```python
image = models.ImageField(...)
```

---

# 34. File upload + normal fields

For multipart/form-data:

```python
data = {
    "name": "Laptop",
    "price": "500.00",
    "stock": "10"
}

with open("laptop.jpg", "rb") as file:

    files = {
        "image": file
    }

    response = requests.post(
        "http://127.0.0.1:8000/api/products/",
        data=data,
        files=files
    )
```

Do not manually set:

```python
Content-Type: multipart/form-data
```

Requests needs to generate the multipart boundary itself.

---

# 35. Downloading files

You can download a file:

```python
response = requests.get(
    "https://example.com/file.pdf"
)

with open("file.pdf", "wb") as file:
    file.write(response.content)
```

For large files, use streaming.

```python
response = requests.get(
    url,
    stream=True
)

with open("file.zip", "wb") as file:

    for chunk in response.iter_content(
        chunk_size=8192
    ):
        if chunk:
            file.write(chunk)
```

---

# 36. URL parameters vs query parameters

Path parameter:

```text
/products/10/
```

Query parameters:

```text
/products/?name=laptop
```

For a path parameter:

```python
url = f"http://127.0.0.1:8000/products/{product_id}/"

response = requests.get(url)
```

For query parameters:

```python
params = {
    "name": "laptop"
}

response = requests.get(
    "http://127.0.0.1:8000/products/",
    params=params
)
```

---

# 37. Authentication with Basic Auth

Requests supports Basic Authentication:

```python
from requests.auth import HTTPBasicAuth

response = requests.get(
    url,
    auth=HTTPBasicAuth(
        "username",
        "password"
    )
)
```

There is also shorthand:

```python
response = requests.get(
    url,
    auth=("username", "password")
)
```

---

# 38. Bearer token helper

You can create the header yourself:

```python
headers = {
    "Authorization": f"Bearer {token}"
}
```

Then:

```python
response = requests.get(
    url,
    headers=headers
)
```

This is the common approach for JWT APIs.

---

# 39. Request JSON and response JSON

A very common API pattern is:

```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/api/products/",
    json={
        "name": "Phone",
        "price": 300,
        "stock": 15
    }
)

print(response.status_code)

data = response.json()

print(data)
```

The complete flow is:

```text
Python dictionary
      ↓
json=
      ↓
HTTP POST
      ↓
Django REST Framework
      ↓
Serializer
      ↓
Database
      ↓
JSON response
      ↓
response.json()
      ↓
Python dictionary
```

---

# 40. Testing your Django API with Requests

Suppose your Django API runs at:

```text
http://127.0.0.1:8000
```

### GET products

```python
import requests

response = requests.get(
    "http://127.0.0.1:8000/api/products/"
)

print(response.status_code)
print(response.json())
```

### Create product

```python
response = requests.post(
    "http://127.0.0.1:8000/api/products/",
    json={
        "name": "Keyboard",
        "price": 50,
        "stock": 20
    }
)

print(response.status_code)
print(response.json())
```

### Update

```python
response = requests.patch(
    "http://127.0.0.1:8000/api/products/1/",
    json={
        "price": 60
    }
)

print(response.status_code)
print(response.json())
```

### Delete

```python
response = requests.delete(
    "http://127.0.0.1:8000/api/products/1/"
)

print(response.status_code)
```

---

# 41. Complete JWT API example

```python
import requests

BASE_URL = "http://127.0.0.1:8000"


# 1. LOGIN
login_response = requests.post(
    f"{BASE_URL}/api/token/",
    json={
        "username": "nzegge",
        "password": "12345678"
    }
)

login_response.raise_for_status()

tokens = login_response.json()

access_token = tokens["access"]


# 2. CREATE AUTHORIZATION HEADER
headers = {
    "Authorization": f"Bearer {access_token}"
}


# 3. GET ORDERS
response = requests.get(
    f"{BASE_URL}/api/orders/",
    headers=headers
)

response.raise_for_status()

orders = response.json()

print(orders)
```

---

# 42. `requests.request()`

There is also a general method:

```python
requests.request()
```

For example:

```python
response = requests.request(
    "GET",
    "https://example.com"
)
```

You can specify the method dynamically:

```python
method = "POST"

response = requests.request(
    method,
    url,
    json=data
)
```

This is useful when the HTTP method comes from a variable.

Normally, however, these are clearer:

```python
requests.get()
requests.post()
requests.put()
requests.patch()
requests.delete()
```

---

# 43. Important `requests` function arguments

Many Requests methods support arguments such as:

```python
requests.get(
    url,
    params=None,
    headers=None,
    cookies=None,
    files=None,
    auth=None,
    timeout=None,
    allow_redirects=True,
    stream=False,
    verify=True
)
```

Common ones:

| Argument          | Purpose                          |
| ----------------- | -------------------------------- |
| `url`             | URL to contact                   |
| `params`          | Query parameters                 |
| `data`            | Form/body data                   |
| `json`            | JSON body                        |
| `headers`         | HTTP headers                     |
| `cookies`         | Cookies                          |
| `files`           | File uploads                     |
| `auth`            | Authentication                   |
| `timeout`         | Maximum waiting time             |
| `allow_redirects` | Follow redirects                 |
| `stream`          | Stream response                  |
| `verify`          | TLS/SSL certificate verification |

---

# 44. `allow_redirects`

Requests normally follows redirects.

```python
response = requests.get(
    url,
    allow_redirects=True
)
```

To prevent following redirects:

```python
response = requests.get(
    url,
    allow_redirects=False
)
```

Then you can inspect the redirect response yourself.

---

# 45. SSL verification

Requests verifies HTTPS certificates by default:

```python
verify=True
```

You may see:

```python
requests.get(
    url,
    verify=False
)
```

This disables certificate verification.

Avoid doing this in production unless you understand why you need it, because it weakens HTTPS security.

---

# 46. A reusable API helper

Instead of repeating code:

```python
response = requests.get(...)
response.raise_for_status()
data = response.json()
```

you can create a helper:

```python
import requests


def get_products():

    response = requests.get(
        "http://127.0.0.1:8000/api/products/",
        timeout=10
    )

    response.raise_for_status()

    return response.json()
```

Then:

```python
products = get_products()

print(products)
```

---

# 47. Recommended error-handling pattern

For API clients:

```python
import requests


try:

    response = requests.get(
        "http://127.0.0.1:8000/api/products/",
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    print(data)

except requests.Timeout:
    print("The request timed out.")

except requests.ConnectionError:
    print("Could not connect to the server.")

except requests.HTTPError as error:
    print("HTTP error:", error)

except requests.RequestException as error:
    print("Request error:", error)
```

This separates different types of failures.

---

# 48. `requests` vs Django test client

This distinction is important for your Django learning.

### Requests

```python
import requests

requests.get(
    "http://127.0.0.1:8000/api/products/"
)
```

This makes a **real HTTP request** to a running server.

You normally need:

```bash
python manage.py runserver
```

### Django test client

```python
self.client.get("/api/products/")
```

This is used inside Django tests and does not require you to manually run the development server.

### DRF `APITestCase`

```python
response = self.client.get(
    "/api/products/"
)
```

This is particularly useful for testing DRF APIs.

---

# 49. Requests vs curl vs Postman

You have several ways to communicate with your API:

```text
Postman
   ↓
GUI API client

curl
   ↓
Command-line API client

requests
   ↓
Python API client

APITestCase
   ↓
Automated Django/DRF testing
```

For example, the same GET request can be made with:

### curl

```bash
curl http://127.0.0.1:8000/api/products/
```

### Requests

```python
requests.get(
    "http://127.0.0.1:8000/api/products/"
)
```

### DRF test

```python
self.client.get(
    "/api/products/"
)
```

---

# 50. The most important things to memorize

For normal API work, focus on these first:

```python
import requests
```

### GET

```python
requests.get(url)
```

### POST

```python
requests.post(url, json=data)
```

### PUT

```python
requests.put(url, json=data)
```

### PATCH

```python
requests.patch(url, json=data)
```

### DELETE

```python
requests.delete(url)
```

### Query parameters

```python
requests.get(
    url,
    params={"name": "laptop"}
)
```

### Headers

```python
requests.get(
    url,
    headers={"Authorization": f"Bearer {token}"}
)
```

### JSON response

```python
response.json()
```

### Status

```python
response.status_code
```

### Error checking

```python
response.raise_for_status()
```

### Timeout

```python
requests.get(
    url,
    timeout=10
)
```

### Session

```python
session = requests.Session()
```

---

# 51. Mental model

The most useful way to understand Requests is:

```text
                 REQUEST
                    │
                    ↓
        ┌─────────────────────┐
        │      requests       │
        │                     │
        │ GET / POST / PUT    │
        │ PATCH / DELETE      │
        │                     │
        │ headers             │
        │ params              │
        │ json                │
        │ files               │
        │ auth                │
        └──────────┬──────────┘
                   │
                   ↓
              HTTP SERVER
                   │
                   ↓
               RESPONSE
                   │
        ┌──────────┴──────────┐
        ↓          ↓           ↓
   status_code   headers    body
                              │
                              ↓
                       response.json()
```

The key distinction is:

```text
requests.get()
       ↓
SEND REQUEST

response
       ↓
RECEIVE RESPONSE
```

And:

```python
response.json()
```

converts a JSON response into normal Python data such as:

```python
dict
list
str
int
bool
None
```

# Quick Cheat Sheet

```python
import requests


# GET
response = requests.get(url)


# GET + query parameters
response = requests.get(
    url,
    params={"search": "phone"}
)


# POST JSON
response = requests.post(
    url,
    json=data
)


# PUT JSON
response = requests.put(
    url,
    json=data
)


# PATCH JSON
response = requests.patch(
    url,
    json=data
)


# DELETE
response = requests.delete(url)


# Headers
response = requests.get(
    url,
    headers={
        "Authorization": f"Bearer {token}"
    }
)


# Response
response.status_code
response.text
response.content
response.json()
response.headers
response.url
response.cookies
response.ok


# Error checking
response.raise_for_status()


# Timeout
response = requests.get(
    url,
    timeout=10
)


# Exception handling
try:
    response = requests.get(
        url,
        timeout=10
    )
    response.raise_for_status()

except requests.RequestException as error:
    print(error)


# Session
session = requests.Session()

session.headers.update({
    "Authorization": f"Bearer {token}"
})

response = session.get(url)
```
