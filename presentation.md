
# Python, a short hike


### PyBCN 🐍 2024/02/21
_Itxaso (Txas) Aizpurua_



---
# Summary 

A short hike up pytest hill, featuring:
- Python testing basics (unittest) (5 min)
- How pytest makes our lives easier (10 min)
- Nice pytest features (plugins, fixtures) (10 min)
- Share Tips & Tricks (10 min)



---

# Python Testing Basics

- We will only discuss unit tests!
- Python unit testing: Unittest

---

# Example 01 - Add
 
---

```python
# main.py

def add_arguments(a, b):
    return a + b
```

---

```python
# main.py

def add_arguments(a, b):
    return a + b

```

```python
# test.py

from unittest import TestCase
from main import add_arguments

class TestCase01(TestCase):

    def test_add_numbers(self):
        return_value = add_arguments(1, 2)
        self.assertEqual(return_value, 3)

```

---

# Live Demo

---

# Example 02 - Cat Facts! :3c 
 
---

```python
# main.py

import requests

def get_random_cat_fact():
    response = requests.get("https://catfact.ninja/fact")
    return response.json()
```

---

# See it in action!

---

```python
# test.py
from unittest import TestCase
from main import get_random_cat_fact

class TestCase02(TestCase):  

    def test_get_random_cat_fact(self):
        return_value = get_random_cat_fact()

        self.assertTrue(len(return_value) > 0)  
```

---

Sometimes we have to **think laterally**.
Can't test for randomness? 
- Test there's at least something.
- Test there are no exceptions.
- Test for invariants.
- ...

---

Testing for randomness is hard.
 -> Remove randomness from the equation.

Enter: **Fixtures** and **Mocks**

---

# Fixture (a.k.a. context, setup and teardown, ...)

That which ensures that there is a **well known** and **fixed** environment in which tests are run so that results are repeatable.

(src: Wikipedia <3)

---

# Mocks 

A method/object that **simulates the behavior** of a real method/object in controlled ways.
Some nuance in difference with Stubs, we'll use them interchangeably.
-> read Martin Fowler's "Mocks Aren't Stubs"!

src: [This SO Post](https://stackoverflow.com/a/21598056) <3

---

Now:
- Remove randomness by using a **mock** on the API request.
- Setup that mock with a **fixture**.


---

```python
from unittest import TestCase
from unittest import mock

from main import get_random_cat_fact

class TestCase02Mocked(TestCase):  
    
    def setUp(self):
        self.mock_requests_patch = mock.patch("main.requests")
        self.mock_requests_object = self.mock_requests_patch.start() # mock starts

    def test_add_numbers(self):
        # We set requests.get().json()'s return value
        self.mock_requests_object.get.return_value.json.return_value = {"fact": "Cats are amazing!"}

        return_value = get_random_cat_fact()

        self.assertEqual(return_value, "Cats are amazing!")

    def tearDown(self):
        self.mock_requests_patch.stop() # mock stops

```

---

# Fun with Mocks

- Part of stdlib: unittest.mock
- Create mock objects with `Mock` or `MagicMock`
- Patch existing objects/references with `patch`
- Sensible defaults do 90% of the work -> we declare the remaining 10%

---

# Fun with mocks
## Patch vs Mock

```python
    def setUp(self):
        self.mock_requests_patch = mock.patch("main.requests")
        print(self.mock_requests_patch)  # controls how patching works

        self.mock_requests_object = self.mock_requests_patch.start() # mock starts
        print(self.mock_requests_object) # controls the behavior of the mock
```

```fish
$ python -m unittest test_mock.py
<unittest.mock._patch object at 0x78719884ab70>
<MagicMock name='requests' id='132429288924336'>
...
```

---

# Fun with Mocks

### Context managers
- start/stop on `__enter__/__exit__`:
```python
    def test_add_numbers(self):
        with mock.patch("main.requests") as mock_requests:
            mock_requests.get.return_value.json.return_value = {"fact": "Cats are amazing!"}
            return_value = get_random_cat_fact()

        self.assertEqual(return_value, "Cats are amazing!")
```
---

# Fun with Mocks

### mock.patch.stopall
- stops all mocks - useful to kill rogue mocks
```python
    def tearDown(self):
        mock.patch.stopall() # instead of self.mock_foo.
```
---

Theres more, but let's jump onto Pytest!

---

# Enter Pytest

