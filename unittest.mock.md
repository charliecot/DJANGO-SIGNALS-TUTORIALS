# Python `unittest.mock` — Complete Guide

## 1. What problem does mocking solve?

Imagine your Django view does this:

```python
import requests

def get_post(request):
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts/1"
    )

    return JsonResponse(response.json())
```

When you test this view, you could let it make the real internet request.

But that creates problems.

Your test now depends on:

```text
Your test
   ↓
Internet
   ↓
jsonplaceholder.typicode.com
   ↓
External server
```

What if:

* your internet is down?
* the external server is down?
* the server is slow?
* the API changes?
* the API returns something unexpected?
* the external API has rate limits?

Your test could fail even though **your Django code is correct**.

Mocking solves this.

Instead:

```text
Your test
   ↓
Mock requests.get()
   ↓
Fake response
```

Now your test controls exactly what `requests.get()` does.

---

# 2. What is a Mock?

A `Mock` is an object that can pretend to be another object or function.

You can tell it:

```text
"When somebody calls you, return this."

"When somebody calls you, raise this exception."

"Remember that you were called."

"Remember what arguments you received."
```

For example:

```python
from unittest.mock import Mock

mock_function = Mock()

mock_function.return_value = 100

result = mock_function()

print(result)
```

Output:

```text
100
```

The real function was never called.

---

# 3. Importing Mock

```python
from unittest.mock import Mock
```

Example:

```python
mock = Mock()

print(mock)
```

A Mock can be called like a normal function:

```python
mock()
```

and it can have methods/attributes:

```python
mock.name
mock.method()
mock.response
```

Mocks dynamically create child mocks when needed.

---

# 4. The most important Mock concepts

You should learn these first:

```text
Mock
patch
return_value
side_effect

assert_called()
assert_called_once()
assert_called_with()
assert_called_once_with()
assert_any_call()
assert_not_called()

call_count
called
call_args
call_args_list
```

These form the core of everyday mocking.

---

# 5. `return_value`

`return_value` means:

> "When this mock is called, return this value."

Example:

```python
from unittest.mock import Mock

mock = Mock()

mock.return_value = "Hello"

result = mock()

print(result)
```

Output:

```text
Hello
```

Conceptually:

```python
mock()
```

becomes:

```python
"Hello"
```

The official documentation defines `return_value` as the value returned when the mock is called.

---

# 6. Example with a function

Imagine the real function is:

```python
def calculate_price():
    return 500
```

Instead of calling it:

```python
result = calculate_price()
```

a test could use:

```python
mock_calculate = Mock()

mock_calculate.return_value = 500

result = mock_calculate()
```

The test now controls the result.

---

# 7. `side_effect`

`side_effect` is extremely important.

It can be used to:

1. raise an exception
2. return different values on successive calls
3. execute another function when the mock is called

The official Python documentation describes all three behaviors.

---

# 8. `side_effect` for exceptions

Suppose the real function might fail:

```python
requests.get(...)
```

You want to test what your application does when the request fails.

You can do:

```python
mock_get.side_effect = requests.exceptions.RequestException
```

Now:

```python
mock_get()
```

raises:

```text
RequestException
```

It behaves as if the real HTTP request failed.

You can also use an exception instance:

```python
mock_get.side_effect = requests.exceptions.RequestException(
    "Connection failed"
)
```

---

# 9. `side_effect` with multiple results

You can give `side_effect` a list:

```python
mock = Mock()

mock.side_effect = [10, 20, 30]

print(mock())
print(mock())
print(mock())
```

Output:

```text
10
20
30
```

So:

```text
1st call → 10
2nd call → 20
3rd call → 30
```

Python's documentation supports iterable `side_effect` values for successive calls.

---

# 10. `side_effect` with a function

You can also give it a function:

```python
def multiply(value):
    return value * 2


mock = Mock()

mock.side_effect = multiply

print(mock(5))
```

Output:

```text
10
```

The function receives the same arguments given to the mock.

---

# 11. `patch()`

This is the most important part for your Django example.

Import:

```python
from unittest.mock import patch
```

`patch()` temporarily replaces an object with a mock.

For example:

```python
@patch("products.views.requests.get")
def test_something(mock_get):
    ...
```

This means:

> During this test, replace `requests.get` as used by `products.views` with a mock.

After the test finishes, the original function is restored.

---

# 12. Why patch?

Suppose your Django view contains:

```python
# products/views.py

import requests

response = requests.get(url)
```

Your test can replace it:

```python
@patch("products.views.requests.get")
```

Now:

```python
requests.get(...)
```

inside `products.views` is no longer the real HTTP function.

It is a mock.

Conceptually:

```text
BEFORE

products.views
      ↓
requests.get()
      ↓
Internet


DURING TEST

products.views
      ↓
MOCK requests.get()
      ↓
Fake response
```

---

# 13. The most important rule about patching

Patch **where the object is used**, not necessarily where it originally came from.

If your view says:

```python
# products/views.py

import requests

requests.get(...)
```

then patch:

```python
@patch("products.views.requests.get")
```

not:

```python
@patch("requests.get")
```

Why?

Because your view has its own reference:

```text
products.views.requests.get
```

That is the object your code actually uses.

This is one of the most important rules in `unittest.mock`.

---

# 14. The mock argument

When you write:

```python
@patch("products.views.requests.get")
def test_post_view_success(self, mock_get):
```

`patch()` gives your test method the mock object.

So:

```python
mock_get
```

represents the patched:

```python
requests.get
```

Inside the test you can control it:

```python
mock_get.return_value = ...
```

and inspect it:

```python
mock_get.assert_called_once_with(...)
```

---

# 15. Understanding `return_value` with `requests`

This is very important.

Your actual code does:

```python
response = requests.get(url)
```

Because `requests.get` has been replaced by `mock_get`:

```python
response = mock_get(url)
```

And because `mock_get.return_value` is the fake response:

```text
mock_get()
   ↓
mock_get.return_value
   ↓
fake response
```

Therefore:

```python
mock_get.return_value.status_code = 200
```

means:

```python
response.status_code
```

will become:

```text
200
```

---

# 16. Why `mock_get.return_value.json.return_value`?

This looks complicated:

```python
mock_get.return_value.json.return_value = return_data
```

But break it down.

Your real code probably does:

```python
response = requests.get(url)

data = response.json()
```

After mocking:

```text
requests.get()
     ↓
mock_get()
     ↓
mock_get.return_value
     ↓
response
```

Then:

```python
response.json()
```

becomes:

```python
mock_get.return_value.json()
```

And you want:

```python
response.json()
```

to return your fake JSON data.

So:

```python
mock_get.return_value.json.return_value = return_data
```

means:

```text
mock_get()
        ↓
fake response
        ↓
.json()
        ↓
return return_data
```

This is one of the most important mocking patterns to understand.

---

# 17. Your `return_data`

You have:

```python
return_data = {
    "userId": 1,
    "id": 1,
    "title": "Test Title",
    "body": "Test Body"
}
```

This pretends that the external API returned:

```json
{
    "userId": 1,
    "id": 1,
    "title": "Test Title",
    "body": "Test Body"
}
```

You are creating fake external API data.

---

# 18. `assert_called_once_with()`

This:

```python
mock_get.assert_called_once_with(
    "https://jsonplaceholder.typicode.com/posts/1"
)
```

checks two things:

### 1. Was `requests.get()` called?

Yes.

### 2. Was it called exactly once with this URL?

It expects:

```python
requests.get(
    "https://jsonplaceholder.typicode.com/posts/1"
)
```

The assertion fails if:

```python
requests.get(url)
```

was never called.

It also fails if it was called twice.

And it fails if the URL was wrong.

Python's documentation defines `assert_called_once_with()` as checking both the exact single-call count and the supplied arguments.

---

# 19. Difference between Mock assertions

## `assert_called()`

Checks that it was called at least once.

```python
mock.assert_called()
```

---

## `assert_called_once()`

Checks that it was called exactly once.

```python
mock.assert_called_once()
```

---

## `assert_called_with()`

Checks the most recent call.

```python
mock.assert_called_with(10)
```

---

## `assert_called_once_with()`

Checks:

```text
called exactly once
+
called with these arguments
```

```python
mock.assert_called_once_with(10)
```

---

## `assert_any_call()`

Checks that the mock was called with particular arguments at least once, even if other calls also occurred.

```python
mock(1)
mock(2)
mock(3)

mock.assert_any_call(2)
```

This passes.

---

## `assert_not_called()`

Checks that the mock was never called.

```python
mock.assert_not_called()
```

These distinctions are documented by Python's `unittest.mock` API.

---

# 20. `called`

You can inspect whether it was called:

```python
mock.called
```

Example:

```python
mock = Mock()

print(mock.called)
```

Output:

```text
False
```

Then:

```python
mock()

print(mock.called)
```

Output:

```text
True
```

---

# 21. `call_count`

You can see how many times it was called:

```python
mock.call_count
```

Example:

```python
mock = Mock()

mock()
mock()
mock()

print(mock.call_count)
```

Output:

```text
3
```

---

# 22. `call_args`

This tells you the arguments from the most recent call.

```python
mock("hello", age=20)

print(mock.call_args)
```

You can use:

```python
mock.call_args
```

to inspect the call.

---

# 23. `call_args_list`

This records all calls.

```python
mock(1)
mock(2)
mock(3)

print(mock.call_args_list)
```

Conceptually:

```text
call(1)
call(2)
call(3)
```

This is useful when your code calls the same dependency multiple times.

---

# 24. `Mock` vs `MagicMock`

You may encounter:

```python
from unittest.mock import Mock, MagicMock
```

`MagicMock` is a subclass-like extension of `Mock` that also supports many Python magic methods automatically.

For example:

```python
mock.__len__()
mock.__str__()
mock.__iter__()
```

In normal Django API mocking, you will frequently use:

```python
Mock
MagicMock
patch
```

You don't need to master every magic method before learning normal mocking.

---

# 25. `patch.object()`

You can patch an attribute on a specific object/class.

Example:

```python
@patch.object(MyClass, "method")
def test_method(mock_method):
    ...
```

This is useful when you already have the object/class available.

---

# 26. `patch()` as a context manager

You don't have to use it as a decorator.

You can write:

```python
with patch("products.views.requests.get") as mock_get:

    mock_get.return_value.status_code = 200

    response = self.client.get(...)
```

The patch exists only inside the `with` block.

After the block, the real function is restored.

---

# 27. `patch()` as a decorator

Your example uses:

```python
@patch("products.views.requests.get")
def test_post_view_success(self, mock_get):
```

The patch exists for the duration of the test method.

Conceptually:

```text
start test
    ↓
replace requests.get with Mock
    ↓
run test
    ↓
restore real requests.get
    ↓
end test
```

---

# 28. `autospec`

You may encounter:

```python
@patch(
    "products.views.requests.get",
    autospec=True
)
```

`autospec` makes the mock more closely follow the signature/specification of the real object.

This can help catch incorrect calls to mocked functions.

It is useful as your testing becomes more advanced.

---

# 29. Now let's study YOUR example

Your test:

```python
class PostsViewTest(TestCase):

    @patch("products.views.requests.get")
    def test_post_view_success(self, mock_get):

        mock_get.return_value.status_code = 200

        return_data = {
            "userId": 1,
            "id": 1,
            "title": "Test Title",
            "body": "Test Body"
        }

        mock_get.return_value.json.return_value = return_data

        response = self.client.get(reverse("post"))

        self.assertJSONEqual(
            response.content,
            return_data
        )

        mock_get.assert_called_once_with(
            "https://jsonplaceholder.typicode.com/posts/1"
        )
```

Let's go through it from the lowest level.

---

# 30. The test class

```python
class PostsViewTest(TestCase):
```

This creates a Django test class.

`TestCase` comes from:

```python
from django.test import TestCase
```

You can use Django's test client:

```python
self.client
```

That's why you can do:

```python
self.client.get(...)
```

---

# 31. The patch decorator

```python
@patch("products.views.requests.get")
```

This says:

> Temporarily replace the `requests.get` used by `products.views` with a mock.

You are NOT going to the real:

```text
https://jsonplaceholder.typicode.com
```

during this test.

Instead:

```text
products.views.requests.get
              ↓
           MOCK
```

---

# 32. The `mock_get` parameter

```python
def test_post_view_success(self, mock_get):
```

`patch()` creates the mock and passes it into your test.

Therefore:

```python
mock_get
```

represents the fake:

```python
requests.get
```

---

# 33. This line

```python
mock_get.return_value.status_code = 200
```

means:

```text
When requests.get() is called,
give the view a fake response.

That fake response has:

response.status_code == 200
```

Think:

```text
mock_get
   │
   │ called
   ↓
return_value
   │
   ├── status_code = 200
   │
   └── json()
```

---

# 34. Your fake API response

You create:

```python
return_data = {
    "userId": 1,
    "id": 1,
    "title": "Test Title",
    "body": "Test Body"
}
```

This is pretending to be the external API's JSON response.

---

# 35. This line

```python
mock_get.return_value.json.return_value = return_data
```

is probably the hardest line.

Break it apart:

### Step 1

```python
mock_get
```

is the fake:

```python
requests.get
```

### Step 2

```python
mock_get.return_value
```

is the fake response.

Equivalent conceptually to:

```python
response = requests.get(url)
```

### Step 3

```python
mock_get.return_value.json
```

is the fake `response.json` method.

### Step 4

```python
mock_get.return_value.json.return_value
```

means:

> What should `response.json()` return?

### Step 5

```python
= return_data
```

means:

> Make `response.json()` return `return_data`.

So:

```python
response.json()
```

will effectively produce:

```python
{
    "userId": 1,
    "id": 1,
    "title": "Test Title",
    "body": "Test Body"
}
```

---

# 36. This line

```python
response = self.client.get(reverse("post"))
```

has two separate operations.

First:

```python
reverse("post")
```

finds the URL named:

```python
post
```

For example:

```text
/post/
```

Then:

```python
self.client.get(...)
```

sends a GET request to your Django view.

So:

```text
reverse("post")
       ↓
"/post/"
       ↓
self.client.get("/post/")
       ↓
Django view
```

---

# 37. What happens inside your Django view?

Your view probably does something similar to:

```python
def post(request):

    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts/1"
    )

    if response.status_code == 200:
        return JsonResponse(response.json())

    return JsonResponse(
        {"error": "Something went wrong"},
        status=503
    )
```

But because of:

```python
@patch("products.views.requests.get")
```

the actual flow is:

```text
Django view
    ↓
requests.get(...)
    ↓
NOT the real requests.get()
    ↓
mock_get(...)
    ↓
mock_get.return_value
    ↓
fake response
```

---

# 38. `status_code`

Your view asks:

```python
response.status_code
```

The mock gives:

```python
200
```

because you configured:

```python
mock_get.return_value.status_code = 200
```

Therefore the view thinks:

> "The external API request succeeded."

---

# 39. `response.json()`

The view then probably does:

```python
response.json()
```

The mock returns:

```python
return_data
```

because you configured:

```python
mock_get.return_value.json.return_value = return_data
```

Therefore your Django view returns the fake API data.

---

# 40. `assertJSONEqual`

You have:

```python
self.assertJSONEqual(
    response.content,
    return_data
)
```

This checks that the Django response contains JSON equivalent to:

```python
return_data
```

So you're testing:

```text
Fake external API JSON
        ↓
Django view
        ↓
Django response
        ↓
Does it contain the expected JSON?
```

---

# 41. The final assertion

```python
mock_get.assert_called_once_with(
    "https://jsonplaceholder.typicode.com/posts/1"
)
```

This verifies your view actually called the external API with the correct URL.

It checks:

```text
Was requests.get called?
        ↓
Yes

Was it called exactly once?
        ↓
Yes

Was the URL correct?
        ↓
Yes
```

This is very important.

Your test isn't just checking the final response.

It is also checking the **interaction between your view and the external service**.

---

# 42. Now your failure test

Your second test is:

```python
@patch("products.views.requests.get")
def test_post_view_fails(self, mock_get):

    mock_get.side_effect = requests.exceptions.RequestException

    response = self.client.get(reverse("post"))

    self.assertEqual(response.status_code, 503)

    mock_get.assert_called_once_with(
        "https://jsonplaceholder.typicode.com/posts/1"
    )
```

This tests a completely different situation.

The first test says:

```text
External API works.
```

The second says:

```text
External API fails.
```

---

# 43. `side_effect` in your failure test

This line:

```python
mock_get.side_effect = requests.exceptions.RequestException
```

means:

> When the view calls `requests.get()`, pretend that a `RequestException` occurred.

Therefore:

```python
mock_get(
    "https://jsonplaceholder.typicode.com/posts/1"
)
```

does NOT return a response.

Instead:

```text
RequestException
```

is raised.

---

# 44. Why use `side_effect` instead of `return_value`?

For success:

```python
mock_get.return_value.status_code = 200
```

means:

```text
requests.get()
     ↓
returns response
```

For failure:

```python
mock_get.side_effect = RequestException
```

means:

```text
requests.get()
     ↓
raises RequestException
```

So:

```text
return_value → control what the mock RETURNS

side_effect → control what happens WHEN the mock is called
```

For exceptions, `side_effect` is the correct tool.

---

# 45. What your view should do with the exception

Your view needs to catch it.

For example:

```python
try:

    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts/1"
    )

except requests.exceptions.RequestException:

    return JsonResponse(
        {"error": "External API unavailable"},
        status=503
    )
```

Now your test:

```python
self.assertEqual(
    response.status_code,
    503
)
```

checks that your view correctly handles the failure.

---

# 46. Complete example

### `products/views.py`

```python
import requests

from django.http import JsonResponse


def post(request):

    try:

        response = requests.get(
            "https://jsonplaceholder.typicode.com/posts/1"
        )

        if response.status_code == 200:

            return JsonResponse(
                response.json()
            )

        return JsonResponse(
            {"error": "External API failed"},
            status=503
        )

    except requests.exceptions.RequestException:

        return JsonResponse(
            {"error": "External API unavailable"},
            status=503
        )
```

---

# 47. Complete tests

```python
import requests

from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch


class PostsViewTest(TestCase):

    @patch("products.views.requests.get")
    def test_post_view_success(self, mock_get):

        # Fake HTTP response
        mock_get.return_value.status_code = 200

        # Fake JSON returned by external API
        return_data = {
            "userId": 1,
            "id": 1,
            "title": "Test Title",
            "body": "Test Body"
        }

        # response.json() returns our fake data
        mock_get.return_value.json.return_value = return_data

        # Call Django view
        response = self.client.get(
            reverse("post")
        )

        # Check returned JSON
        self.assertJSONEqual(
            response.content,
            return_data
        )

        # Make sure external API was called correctly
        mock_get.assert_called_once_with(
            "https://jsonplaceholder.typicode.com/posts/1"
        )


    @patch("products.views.requests.get")
    def test_post_view_fails(self, mock_get):

        # Pretend external API request failed
        mock_get.side_effect = (
            requests.exceptions.RequestException
        )

        # Call Django view
        response = self.client.get(
            reverse("post")
        )

        # View should return HTTP 503
        self.assertEqual(
            response.status_code,
            503
        )

        # Make sure API was still called correctly
        mock_get.assert_called_once_with(
            "https://jsonplaceholder.typicode.com/posts/1"
        )
```

---

# 48. The entire success test as a diagram

This is the most important diagram to understand:

```text
TEST
 │
 │ @patch(...)
 ↓
requests.get is replaced
 │
 ↓
mock_get
 │
 │ return_value
 ↓
FAKE RESPONSE
 │
 ├── status_code = 200
 │
 └── json()
       │
       ↓
   return_data
       │
       ↓
Django VIEW
       │
       ↓
JsonResponse(...)
       │
       ↓
self.client.get(...)
       │
       ↓
response
       │
       ↓
assertJSONEqual(...)
```

And separately:

```text
mock_get.assert_called_once_with(URL)
```

checks the communication itself.

---

# 49. The failure test as a diagram

```text
TEST
 │
 │ @patch(...)
 ↓
mock_get
 │
 │ side_effect
 ↓
RequestException
 │
 ↓
Django VIEW catches exception
 │
 ↓
JsonResponse(..., status=503)
 │
 ↓
response.status_code
 │
 ↓
503
```

Then:

```python
mock_get.assert_called_once_with(URL)
```

checks that the API call happened correctly.

---

# 50. Why mocking is useful in real Django projects

You will eventually have views/services that call:

```text
External REST API
Payment gateway
Email service
Cloud storage
Redis
Celery
SMS provider
Authentication provider
Shipping provider
AI API
```

You generally don't want every unit test to communicate with those real systems.

For example:

```python
@patch("payments.services.requests.post")
def test_payment_success(self, mock_post):
    ...
```

You can simulate:

```text
payment success
payment declined
timeout
connection error
500 error
invalid response
```

without actually charging a card.

---

# 51. Mocking email

Suppose:

```python
from django.core.mail import send_mail

send_mail(...)
```

You could test:

```python
@patch("products.views.send_mail")
def test_email(self, mock_send_mail):

    ...

    mock_send_mail.assert_called_once()
```

Now the test doesn't actually send an email.

---

# 52. Mocking Celery

Suppose your code calls:

```python
send_order_email.delay(order.id)
```

You could mock:

```python
@patch("orders.views.send_order_email.delay")
def test_order(self, mock_task):

    ...

    mock_task.assert_called_once_with(order.id)
```

You're testing:

> Did my view send the Celery task?

without actually running the worker.

---

# 53. Mocking a function

Suppose:

```python
# services.py

def calculate_shipping():
    return 500
```

Your view uses:

```python
from .services import calculate_shipping
```

Test:

```python
@patch("orders.views.calculate_shipping")
def test_shipping(self, mock_shipping):

    mock_shipping.return_value = 500

    ...
```

Again:

```text
Real service
     ↓
replaced by
     ↓
Mock
```

---

# 54. `assert_called_once_with()` vs `assertJSONEqual()`

These test different things.

### `assertJSONEqual`

Tests the **result**:

```python
self.assertJSONEqual(
    response.content,
    expected_data
)
```

Question:

> Did my view return the correct JSON?

### `assert_called_once_with`

Tests the **interaction**:

```python
mock_get.assert_called_once_with(url)
```

Question:

> Did my view call the external API correctly?

So your success test checks both:

```text
OUTPUT
+
BEHAVIOR
```

That's excellent testing practice.

---

# 55. `return_value` vs `side_effect`

Memorize this table:

| Feature                     | Meaning                   | Example                           |
| --------------------------- | ------------------------- | --------------------------------- |
| `return_value`              | What mock returns         | `mock.return_value = 200`         |
| `side_effect`               | What happens when called  | `mock.side_effect = Exception`    |
| `called`                    | Was it called?            | `mock.called`                     |
| `call_count`                | Number of calls           | `mock.call_count`                 |
| `assert_called()`           | Called at least once      | `mock.assert_called()`            |
| `assert_called_once()`      | Called exactly once       | `mock.assert_called_once()`       |
| `assert_called_with()`      | Last call had these args  | `mock.assert_called_with(1)`      |
| `assert_called_once_with()` | Exactly once + exact args | `mock.assert_called_once_with(1)` |
| `assert_any_call()`         | Any call matched          | `mock.assert_any_call(1)`         |
| `assert_not_called()`       | Never called              | `mock.assert_not_called()`        |

---

# 56. A very important warning

Mocking can make tests pass even when the real integration is broken.

For example, if you mock:

```python
@patch("products.views.requests.get")
```

your test isn't actually checking whether:

```text
JSONPlaceholder
```

works.

It is checking whether **your Django view behaves correctly given the simulated behavior**.

That's why real integration tests can still be valuable. Python's documentation also notes that mocks can allow tests to continue passing after an API/member is changed, which is one reason integration tests remain useful.

Think:

```text
Unit test
    ↓
Mock external dependency
    ↓
Fast + isolated
```

and:

```text
Integration test
    ↓
Use real components
    ↓
Verify components work together
```

You often want both.

---

# 57. The 5 things I want you to memorize first

Don't try to memorize the entire module immediately.

Start with these:

## 1. `patch`

```python
@patch("module.object")
```

> Replace the real dependency with a mock during the test.

## 2. `return_value`

```python
mock.return_value = value
```

> Tell the mock what to return.

## 3. `side_effect`

```python
mock.side_effect = Exception
```

> Tell the mock to raise an exception.

## 4. `assert_called_once_with`

```python
mock.assert_called_once_with(expected_argument)
```

> Verify exactly one call with the expected arguments.

## 5. Nested `return_value`

```python
mock.return_value.method.return_value = value
```

For your HTTP example:

```python
mock_get.return_value.json.return_value = return_data
```

means:

```text
requests.get()
       ↓
response
       ↓
response.json()
       ↓
return_data
```

---

# 58. Your example in plain English

Your success test says:

> "Replace `requests.get()` with a fake. Pretend the external API returned HTTP 200 and this JSON. Call my Django view. Verify that my view returned that JSON. Also verify that my view called the external API exactly once with the correct URL."

Your failure test says:

> "Replace `requests.get()` with a fake. Pretend the external API raised a `RequestException`. Call my Django view. Verify that my view responds with HTTP 503. Also verify that my view attempted the external API call exactly once with the correct URL."

That is the heart of `unittest.mock`.

---

# 59. Final mental model

When you see:

```python
@patch("products.views.requests.get")
def test_something(self, mock_get):
```

immediately think:

```text
REAL:

requests.get()
     ↓
Internet


TEST:

mock_get()
     ↓
Fake response
```

Then:

```python
mock_get.return_value
```

means:

```text
"What should requests.get() return?"
```

Then:

```python
mock_get.return_value.json.return_value
```

means:

```text
"What should response.json() return?"
```

Then:

```python
mock_get.side_effect
```

means:

```text
"What should happen when requests.get() is called?"
```

And:

```python
mock_get.assert_called_once_with(...)
```

means:

```text
"Did my code call requests.get()
 exactly once
 with exactly these arguments?"
```

Once this mental model becomes natural, mocking Django views, emails, Celery tasks, external APIs, payment services, and other dependencies becomes much easier.
