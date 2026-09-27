# Django Testing: unittest, TestCase, APITestCase and Assertions

## 1. What is Testing?

Testing means:

> **Writing code that automatically checks whether your application behaves as expected.**

For example, suppose you have:

```python
def add(a, b):
    return a + b
```

You expect:

```python
add(2, 3)
```

to return:

```text
5
```

A test can automatically verify this.

```python
self.assertEqual(add(2, 3), 5)
```

If the result is `5`:

```text
TEST PASSES ✅
```

If the result is `6`:

```text
TEST FAILS ❌
```

---

# 2. Why Do We Test?

Imagine your Django API has:

```text
Users
Products
Orders
Authentication
JWT
Permissions
Payments
Emails
```

You manually test everything using Postman every time you change your code.

That becomes difficult.

Automated tests allow you to say:

```text
Run all tests
      ↓
Check 50 things automatically
      ↓
PASS / FAIL
```

For example:

```text
test_user_can_login .............. OK
test_invalid_password ........... OK
test_product_creation ........... OK
test_order_creation ............. OK
test_anonymous_cannot_create .... OK
```

---

# 3. What is `unittest`?

`unittest` is Python's built-in testing framework.

You don't normally need to install it.

```python
import unittest
```

It provides:

* `TestCase`
* assertions
* test discovery
* test setup/teardown
* test running

Example:

```python
import unittest


def add(a, b):
    return a + b


class AddTest(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(2, 3), 5)
```

Here:

```python
unittest.TestCase
```

is the base class for the test.

---

# 4. What is `TestCase`?

`TestCase` is a class that provides tools for writing tests.

Python:

```python
import unittest

class MyTest(unittest.TestCase):
    ...
```

Django also provides its own:

```python
from django.test import TestCase
```

Django's `TestCase` is designed for testing Django applications.

Example:

```python
from django.test import TestCase


class ProductTest(TestCase):

    def test_something(self):
        self.assertEqual(2 + 2, 4)
```

---

# 5. Python `unittest.TestCase` vs Django `TestCase`

These are related but different.

### Python

```python
import unittest

class MyTest(unittest.TestCase):
    ...
```

This is useful for ordinary Python code.

### Django

```python
from django.test import TestCase

class MyTest(TestCase):
    ...
```

Django's `TestCase` gives you Django-specific testing features, especially database testing.

For Django projects, you will commonly use:

```python
from django.test import TestCase
```

---

# 6. What Does Django `TestCase` Give You?

Django's:

```python
TestCase
```

is useful when testing:

* models
* database operations
* forms
* business logic
* Django functions
* authentication logic
* serializers in some cases

Example:

```python
from django.test import TestCase
from core.models import Product


class ProductTest(TestCase):

    def test_create_product(self):

        product = Product.objects.create(
            name="Laptop",
            price=1000
        )

        self.assertEqual(product.name, "Laptop")
        self.assertEqual(product.price, 1000)
```

---

# 7. Test Method Naming

Test methods normally start with:

```python
test_
```

Example:

```python
def test_create_product(self):
    ...
```

Not:

```python
def create_product_test(self):
    ...
```

Although the latter is an ordinary Python method, standard test discovery looks for methods beginning with `test`.

---

# 8. Basic Test Structure

A typical Django test:

```python
from django.test import TestCase


class ProductTest(TestCase):

    def test_product_name(self):

        product = Product.objects.create(
            name="Laptop",
            price=1000
        )

        self.assertEqual(
            product.name,
            "Laptop"
        )
```

Think:

```text
ARRANGE
   ↓
Create/setup data

ACT
   ↓
Run the code

ASSERT
   ↓
Check the result
```

---

# 9. Arrange → Act → Assert

This is one of the most important testing patterns.

## Arrange

Prepare everything:

```python
product = Product.objects.create(
    name="Laptop",
    price=1000
)
```

## Act

Perform the operation:

```python
product.price = 1200
product.save()
```

## Assert

Check the result:

```python
self.assertEqual(product.price, 1200)
```

So:

```text
ARRANGE → prepare
ACT     → perform
ASSERT  → verify
```

---

# 10. What is `APITestCase`?

`APITestCase` comes from Django REST Framework.

```python
from rest_framework.test import APITestCase
```

It is designed specifically for testing APIs.

For example:

```python
class ProductAPITest(APITestCase):
    ...
```

It provides an API test client.

```python
self.client
```

You can use:

```python
self.client.get()
self.client.post()
self.client.put()
self.client.patch()
self.client.delete()
```

---

# 11. Why Use `APITestCase`?

Suppose your API has:

```text
GET /api/products/
POST /api/products/
GET /api/products/1/
PUT /api/products/1/
DELETE /api/products/1/
```

Instead of opening Postman manually, you can test them with Python.

Example:

```python
response = self.client.get("/api/products/")
```

Then:

```python
self.assertEqual(response.status_code, 200)
```

---

# 12. Basic `APITestCase`

```python
from rest_framework.test import APITestCase


class ProductAPITest(APITestCase):

    def test_product_list(self):

        response = self.client.get(
            "/api/products/"
        )

        self.assertEqual(
            response.status_code,
            200
        )
```

This sends an HTTP GET request to your API.

---

# 13. API Client

`self.client` is extremely important.

It simulates a client making requests to your API.

### GET

```python
response = self.client.get("/api/products/")
```

### POST

```python
response = self.client.post(
    "/api/products/",
    data={
        "name": "Laptop",
        "price": "1000.00"
    }
)
```

### PUT

```python
response = self.client.put(
    "/api/products/1/",
    data={
        "name": "New Laptop",
        "price": "1200.00"
    }
)
```

### PATCH

```python
response = self.client.patch(
    "/api/products/1/",
    data={
        "price": "1100.00"
    }
)
```

### DELETE

```python
response = self.client.delete(
    "/api/products/1/"
)
```

---

# 14. What is `response`?

When you do:

```python
response = self.client.get(
    "/api/products/"
)
```

`response` contains information about the API response.

You can inspect:

```python
response.status_code
response.data
response.headers
response.content
```

For DRF, `response.data` is especially useful.

Example:

```python
print(response.data)
```

Could produce:

```python
[
    {
        "id": 1,
        "name": "Laptop",
        "price": "1000.00"
    }
]
```

---

# 15. API Status Code Assertions

You can test:

```python
self.assertEqual(
    response.status_code,
    200
)
```

Common API status codes:

```text
200 OK
201 Created
204 No Content
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
405 Method Not Allowed
409 Conflict
500 Internal Server Error
```

Example:

```python
self.assertEqual(
    response.status_code,
    201
)
```

means:

> I expect the API to successfully create the resource.

---

# 16. What is an Assertion?

An assertion means:

> **Tell the test what result you expect.**

For example:

```python
self.assertEqual(2 + 2, 4)
```

You are saying:

```text
I expect 2 + 2 to equal 4.
```

If true:

```text
PASS ✅
```

If false:

```text
FAIL ❌
```

---

# 17. `assertEqual()`

Checks whether two values are equal.

```python
self.assertEqual(actual, expected)
```

Example:

```python
self.assertEqual(
    product.name,
    "Laptop"
)
```

Meaning:

```text
actual value
     ↓
product.name

expected value
     ↓
"Laptop"
```

---

# 18. `assertNotEqual()`

Checks that two values are NOT equal.

```python
self.assertNotEqual(
    product.price,
    0
)
```

Means:

> The price should not be zero.

---

# 19. `assertTrue()`

Checks that something is `True`.

```python
self.assertTrue(user.is_active)
```

If:

```python
user.is_active == True
```

the test passes.

---

# 20. `assertFalse()`

Checks that something is `False`.

```python
self.assertFalse(user.is_staff)
```

---

# 21. `assertIsNone()`

Checks that a value is `None`.

```python
self.assertIsNone(value)
```

Example:

```python
result = some_function()

self.assertIsNone(result)
```

---

# 22. `assertIsNotNone()`

Checks that a value is NOT `None`.

```python
self.assertIsNotNone(user)
```

Useful when testing that an object was successfully created/found.

---

# 23. `assertIs()`

Checks object identity.

```python
self.assertIs(value1, value2)
```

This means:

> Are these the exact same object?

This is different from:

```python
assertEqual()
```

which checks equality.

---

# 24. `assertIsNot()`

Checks that two objects are not the same object.

```python
self.assertIsNot(
    object1,
    object2
)
```

---

# 25. `assertIn()`

Checks whether something exists inside another object.

```python
self.assertIn("Laptop", names)
```

Example:

```python
names = ["Laptop", "Phone", "Mouse"]

self.assertIn("Laptop", names)
```

Passes.

---

# 26. `assertNotIn()`

Checks that something does not exist inside another object.

```python
self.assertNotIn(
    "Car",
    names
)
```

---

# 27. `assertIsInstance()`

Checks the type/class of an object.

```python
self.assertIsInstance(
    user,
    User
)
```

Meaning:

> `user` should be an instance of `User`.

---

# 28. `assertNotIsInstance()`

Checks that an object is NOT an instance of a class.

```python
self.assertNotIsInstance(
    value,
    str
)
```

---

# 29. `assertRaises()`

Checks that code raises a particular exception.

Suppose:

```python
def divide(a, b):
    return a / b
```

Dividing by zero raises:

```python
ZeroDivisionError
```

Test:

```python
with self.assertRaises(ZeroDivisionError):
    divide(10, 0)
```

This test passes if the exception occurs.

---

# 30. Django Example of `assertRaises()`

```python
from django.test import TestCase


class ProductTest(TestCase):

    def test_invalid_operation(self):

        with self.assertRaises(ValueError):
            raise ValueError("Invalid product")
```

---

# 31. `assertContains()`

Django's test client provides useful response assertions.

For example:

```python
response = self.client.get("/products/")

self.assertContains(
    response,
    "Laptop"
)
```

Meaning:

> The response should contain `"Laptop"`.

---

# 32. `assertNotContains()`

```python
self.assertNotContains(
    response,
    "Secret Product"
)
```

Means:

> The response should NOT contain this text.

---

# 33. `assertRedirects()`

Useful for Django views.

```python
response = self.client.get("/login/")

self.assertRedirects(
    response,
    "/accounts/login/"
)
```

It checks that the response redirected to the expected URL.

---

# 34. `assertTemplateUsed()`

Checks that a Django view used a particular template.

```python
self.assertTemplateUsed(
    response,
    "products/list.html"
)
```

This is more relevant to traditional Django views than DRF APIs.

---

# 35. `assertQuerySetEqual()`

Django provides:

```python
self.assertQuerySetEqual()
```

Useful when testing QuerySets.

Example:

```python
products = Product.objects.all()

self.assertQuerySetEqual(
    products,
    ["Laptop", "Phone"]
)
```

The exact expected values depend on how the queryset is constructed and represented.

---

# 36. `assertNumQueries()`

Very useful for Django database optimization.

```python
with self.assertNumQueries(1):
    Product.objects.all().count()
```

This checks how many database queries are executed.

Useful when investigating:

```text
N+1 queries
select_related()
prefetch_related()
```

---

# 37. `assertLogs()`

Checks logging output.

```python
with self.assertLogs("myapp", level="INFO"):
    ...
```

Useful when your code uses Python logging.

---

# 38. Assertion Groups

It is common to use multiple assertions in one test:

```python
def test_create_product(self):

    response = self.client.post(
        "/api/products/",
        {
            "name": "Laptop",
            "price": "1000.00"
        }
    )

    self.assertEqual(
        response.status_code,
        201
    )

    self.assertEqual(
        response.data["name"],
        "Laptop"
    )

    self.assertEqual(
        response.data["price"],
        "1000.00"
    )
```

This tests several things about the same operation.

---

# 39. Testing Authentication

Since you are using Django REST Framework, authentication tests are very important.

Suppose:

```text
POST /api/products/
```

requires authentication.

You can test an anonymous user:

```python
def test_anonymous_cannot_create_product(self):

    response = self.client.post(
        "/api/products/",
        {
            "name": "Laptop",
            "price": "1000.00"
        }
    )

    self.assertEqual(
        response.status_code,
        401
    )
```

---

# 40. Creating a Test User

```python
from django.contrib.auth import get_user_model

User = get_user_model()
```

Then:

```python
user = User.objects.create_user(
    username="nzegge",
    password="12345678"
)
```

Important:

Use:

```python
create_user()
```

rather than:

```python
User.objects.create(
    username="nzegge",
    password="12345678"
)
```

when creating a normal test user, because `create_user()` properly handles password hashing.

---

# 41. Authenticating the API Client

DRF provides:

```python
self.client.force_authenticate(user=user)
```

Example:

```python
def test_authenticated_user_can_create_product(self):

    user = User.objects.create_user(
        username="nzegge",
        password="12345678"
    )

    self.client.force_authenticate(
        user=user
    )

    response = self.client.post(
        "/api/products/",
        {
            "name": "Laptop",
            "price": "1000.00"
        }
    )

    self.assertEqual(
        response.status_code,
        201
    )
```

---

# 42. `force_authenticate()`

This is very useful in tests.

```python
self.client.force_authenticate(user=user)
```

means:

> Make this API test client act as this authenticated user.

It is commonly used when you want to test permissions/API behavior without testing the login endpoint itself.

---

# 43. Testing JWT Authentication

If you specifically want to test your actual JWT login flow, you can call your token endpoint.

For example:

```python
response = self.client.post(
    "/api/token/",
    {
        "username": "nzegge",
        "password": "12345678"
    }
)
```

Then:

```python
self.assertEqual(
    response.status_code,
    200
)
```

You can inspect:

```python
response.data["access"]
response.data["refresh"]
```

However, for many individual endpoint tests, `force_authenticate()` is simpler because it focuses the test on the endpoint rather than making every test depend on the login implementation.

---

# 44. Testing Permissions

Suppose only authenticated users can access:

```text
GET /api/orders/
```

Test anonymous:

```python
def test_anonymous_user_cannot_access_orders(self):

    response = self.client.get(
        "/api/orders/"
    )

    self.assertEqual(
        response.status_code,
        401
    )
```

Then authenticated:

```python
def test_authenticated_user_can_access_orders(self):

    user = User.objects.create_user(
        username="nzegge",
        password="12345678"
    )

    self.client.force_authenticate(
        user=user
    )

    response = self.client.get(
        "/api/orders/"
    )

    self.assertEqual(
        response.status_code,
        200
    )
```

---

# 45. Testing the Database

You can test that an object was actually created.

```python
self.client.post(
    "/api/products/",
    {
        "name": "Laptop",
        "price": "1000.00"
    }
)

self.assertTrue(
    Product.objects.filter(
        name="Laptop"
    ).exists()
)
```

You can also check:

```python
self.assertEqual(
    Product.objects.count(),
    1
)
```

---

# 46. `setUp()`

`setUp()` runs before each test method.

Example:

```python
class ProductTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="nzegge",
            password="12345678"
        )

        self.product = Product.objects.create(
            name="Laptop",
            price=1000
        )
```

Then every test can use:

```python
self.user
self.product
```

Example:

```python
def test_product_name(self):

    self.assertEqual(
        self.product.name,
        "Laptop"
    )
```

---

# 47. Why `setUp()` Is Useful

Without `setUp()`:

```python
def test_one(self):
    user = ...
    product = ...

def test_two(self):
    user = ...
    product = ...

def test_three(self):
    user = ...
    product = ...
```

You repeat yourself.

With `setUp()`:

```python
def setUp(self):
    self.user = ...
    self.product = ...
```

Every test gets the required test data.

---

# 48. `tearDown()`

`tearDown()` runs after each test.

```python
def tearDown(self):
    ...
```

It is used for cleanup when needed.

Django's test framework already handles its test database lifecycle, so you should not manually delete normal test database records just because a test ends.

---

# 49. `setUpTestData()`

Django also provides:

```python
@classmethod
def setUpTestData(cls):
    ...
```

Example:

```python
class ProductTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.product = Product.objects.create(
            name="Laptop",
            price=1000
        )
```

This is useful for test data that can be shared across test methods without recreating it for every test.

---

# 50. `TestCase` vs `APITestCase`

### Django `TestCase`

```python
from django.test import TestCase
```

Use it mainly for:

```text
Models
Database
Forms
Business logic
Django views
```

### DRF `APITestCase`

```python
from rest_framework.test import APITestCase
```

Use it mainly for:

```text
REST APIs
HTTP requests
API responses
Authentication
Permissions
Status codes
JSON/API data
```

---

# 51. Big Picture

Think about the hierarchy/conceptual relationship like this:

```text
Python unittest
       │
       ↓
unittest.TestCase
       │
       ├── Django TestCase
       │       │
       │       └── Database/Django testing
       │
       └── DRF APITestCase
               │
               └── API testing
```

The exact inheritance implementation should be thought of in terms of the frameworks involved, but for learning purposes the important point is that Django/DRF provide specialized test classes on top of Python's testing ecosystem.

---

# 52. Most Important Assertions Cheat Sheet

```python
# Equal
self.assertEqual(a, b)

# Not equal
self.assertNotEqual(a, b)

# True
self.assertTrue(value)

# False
self.assertFalse(value)

# None
self.assertIsNone(value)

# Not None
self.assertIsNotNone(value)

# Same object
self.assertIs(a, b)

# Different objects
self.assertIsNot(a, b)

# Exists inside
self.assertIn(value, container)

# Does not exist inside
self.assertNotIn(value, container)

# Correct type
self.assertIsInstance(value, SomeClass)

# Wrong/different type
self.assertNotIsInstance(value, SomeClass)

# Expected exception
with self.assertRaises(SomeException):
    function()

# Response contains text
self.assertContains(response, "text")

# Response does not contain text
self.assertNotContains(response, "text")

# Redirect
self.assertRedirects(response, "/expected-url/")

# Template
self.assertTemplateUsed(response, "template.html")

# Number of DB queries
with self.assertNumQueries(2):
    ...
```

---

# 53. API Testing Cheat Sheet

```python
from rest_framework.test import APITestCase


class ProductAPITest(APITestCase):

    def test_list_products(self):

        response = self.client.get(
            "/api/products/"
        )

        self.assertEqual(
            response.status_code,
            200
        )
```

POST:

```python
response = self.client.post(
    "/api/products/",
    {
        "name": "Laptop",
        "price": "1000.00"
    }
)
```

PUT:

```python
response = self.client.put(
    "/api/products/1/",
    {
        "name": "New Laptop",
        "price": "1200.00"
    }
)
```

PATCH:

```python
response = self.client.patch(
    "/api/products/1/",
    {
        "price": "1100.00"
    }
)
```

DELETE:

```python
response = self.client.delete(
    "/api/products/1/"
)
```

Authentication:

```python
self.client.force_authenticate(
    user=user
)
```

Status:

```python
self.assertEqual(
    response.status_code,
    200
)
```

Response data:

```python
response.data
```

---

# 54. A Complete DRF Example

```python
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from core.models import Product


User = get_user_model()


class ProductAPITest(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="nzegge",
            password="12345678"
        )

        self.product = Product.objects.create(
            name="Laptop",
            price="1000.00"
        )

        self.url = "/api/products/"

    def test_product_list(self):

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            self.url
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_create_product(self):

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            self.url,
            {
                "name": "Phone",
                "price": "500.00"
            }
        )

        self.assertEqual(
            response.status_code,
            201
        )

        self.assertEqual(
            response.data["name"],
            "Phone"
        )

    def test_anonymous_user(self):

        response = self.client.post(
            self.url,
            {
                "name": "Phone",
                "price": "500.00"
            }
        )

        self.assertEqual(
            response.status_code,
            401
        )
```

---

# 55. Running Tests

Django normally discovers tests when they are placed in files such as:

```text
tests.py
```

or a test package containing files such as:

```text
test_models.py
test_views.py
test_serializers.py
test_api.py
```

Run all Django tests:

```bash
python manage.py test
```

Run tests for an app:

```bash
python manage.py test core
```

Run a particular test class:

```bash
python manage.py test core.tests.ProductAPITest
```

Run a particular test method:

```bash
python manage.py test core.tests.ProductAPITest.test_product_list
```

---

# 56. Test Results

You may see:

```text
....
----------------------------------------------------------------------
Ran 4 tests in 0.123s

OK
```

Each:

```text
.
```

usually represents a successful test.

Failure:

```text
F
```

Error:

```text
E
```

So:

```text
.... → all passed
..F. → one test failed
..E. → one test produced an error
```

---

# 57. Failure vs Error

This distinction is useful.

### Failure

Your assertion was false.

Example:

```python
self.assertEqual(2 + 2, 5)
```

The test ran, but the expected result was wrong.

```text
FAIL
```

### Error

Something unexpected happened while running the test.

Example:

```python
user = User.objects.get(username="does-not-exist")
```

If the object doesn't exist and you didn't expect that:

```text
ERROR
```

Simple way to remember:

```text
FAILURE
   ↓
My test expectation was wrong.

ERROR
   ↓
The test/code crashed unexpectedly.
```

---

# 58. The Most Important Mental Model

When writing a test, ask these three questions:

```text
1. What am I testing?
          ↓
2. What result do I expect?
          ↓
3. Which assertion proves that result?
```

Example:

```python
response = self.client.get(
    "/api/products/"
)
```

Question 1:

```text
What am I testing?
→ Product list API
```

Question 2:

```text
What do I expect?
→ HTTP 200
```

Question 3:

```python
self.assertEqual(
    response.status_code,
    200
)
```

That's the heart of automated testing.

---

# 59. Final Memory Map

```text
TESTING
│
├── unittest
│     │
│     └── Python testing framework
│
├── TestCase
│     │
│     └── Test class/base for structured tests
│
├── Django TestCase
│     │
│     └── Django + database testing
│
├── APITestCase
│     │
│     └── Django REST Framework API testing
│
└── ASSERTIONS
      │
      ├── assertEqual()
      ├── assertNotEqual()
      ├── assertTrue()
      ├── assertFalse()
      ├── assertIsNone()
      ├── assertIsNotNone()
      ├── assertIn()
      ├── assertNotIn()
      ├── assertIsInstance()
      ├── assertRaises()
      ├── assertContains()
      ├── assertRedirects()
      └── assertNumQueries()
```

## The three things to remember first

```python
# Django database test
from django.test import TestCase


# DRF API test
from rest_framework.test import APITestCase


# Assertion
self.assertEqual(actual, expected)
```

And for an API:

```python
response = self.client.get("/api/products/")

self.assertEqual(
    response.status_code,
    200
)
```

That single example contains the basic pattern:

```text
client → request → response → assertion
```

Once you understand that pattern, authentication tests, permission tests, serializer tests, order tests, JWT tests, and CRUD tests become much easier to organize.
