<!-- paginate: true -->
# Python, a short hike


### PyBCN 🐍 2024/02/21


_Itxaso (Txas) Aizpurua_

txas@txas.me - github.com/itxasos23 
itxasos@blahaj.social


---

# Introduction

A short hike around Python testing and Pytest
- Junior friendly!
- Focus on Unit Testing
- This is just my toolbox. Yours may be different and thats great!

---

# whoami

```bash
$ whoami
- Itxaso Aizpurua 
- 6 years Python experience 
- 2 years girl experience (Trans rights! 🏳️‍⚧️  🦈)
- Backend Eng @ Livewell (Zurich)
- Full time nerd
- Pytest contributor (2 whole commits!!!)
```

---

# Summary 

A short hike up pytest hill, featuring:
- Python testing basics (unittest) (10 min)
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

# On Testing

Sometimes we have to **think laterally**.
Can't test for randomness? 
- Test there's at least something.
- Test there are no exceptions.
- Test for invariants.
- ...

---

# On Testing

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

# Mocks

Now:
- Remove randomness by using a **mock** on the API request.
- Setup that mock with a **fixture**.


---

# Fixtures and Mocks

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

# Fun with mocks

Mock on reference, not definition

```python
# wrong
with mock.patch("requests") as mock_request:
...

# right
with mock.patch("main.requests") as mock_request:
...
```
You want to mock `main.py`'s use of `requests`, not `requests` itself.

---

# Fun with mocks

Some tips:
- Print the name of the function you want to mock first.
- Mock classes before they're instantiated into objects!
- Beware of import-time code (i.e. code ran on 0-indent), hard to mock.
- Take your time to understand them, they're the key to unit tests.

---

# Enter Pytest

Theres more, but let's jump onto Pytest!

---

## Why pytest?

- Unittest has its limits
- Pytest highlights from the docs:
  - Detailed info on **assert statements**
  - **Auto-discovery** of test modules and functions
  - Modular **fixtures**
  - Rich **plugin** architecture and ecosystem


---

# Fixtures
### Nice Asserts


---

# Nice asserts
### This

```python
self.assertGreater(3, 4)
```
```bash
Traceback (most recent call last):
  File "/home/itxaso/docs/pytest_talk/examples/ex_03/tests.py", line 6, in test_greater
    self.assertGreater(3, 4)
AssertionError: 3 not greater than 4
```
---

# Nice asserts
### Becomes this

```python
assert 3 > 4
```
```bash
self = <tests.TestCase03 testMethod=test_greater_assert>

    def test_greater_assert(self):
>       assert 3 > 4
E       assert 3 > 4
```

No need to memorize self.assert* method names!

---

# Nice asserts

### Assert failure introspection

```python
def test_introspection(self):
    dict_1 = {"key_1": "value_1"}
    dict_2 = {"key_1": "value_2"}

    assert dict_1 == dict_2

```

```bash
>       assert dict_1 == dict_2
E       AssertionError: assert {'key_1': 'value_1'} == {'key_1': 'value_2'}
E
E         Differing items:
E         {'key_1': 'value_1'} != {'key_1': 'value_2'}
E         Use -v to get more diff
```

---

# Pytest
## Fixtures

---

# Fixtures (Pytest)

Remember this?

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

# Fixtures (Pytest)

Now we can do this

```python
from pytest import fixture
from unittest import mock
from main import get_random_cat_fact

@pytest.fixture
def mock_requests():
    with mock.patch("main.requests") as mock_object:
        yield mock_object

def test_add_numbers(mock_requests):
    mock_requests.get.return_value.json.return_value = {"fact": "Cats are amazing!"}
    return_value = get_random_cat_fact()
    assert return_value == "Cats are amazing!"

```

---

# Fixtures (Pytest)

Or this!

```python
# test.py
from main import get_random_cat_fact
# look ma! No import!

def test_add_numbers(mock_requests):
    mock_requests.get.return_value.json.return_value = {"fact": "Cats are amazing!"}
    return_value = get_random_cat_fact()
    assert return_value == "Cats are amazing!"
```

```python 
# conftest.py
from pytest import fixture
from unittest import mock

@pytest.fixture
def mock_requests():
    with mock.patch("main.requests") as mock_object:
        yield mock_object
```

---

# Fixtures (Pytest)

More on fixtures:
- builtin fixtures to capture logs, stdout, etc.
- fixture dependencies
- autouse fixtures
- fixture scopes
- parametrize fixtures



---

# Pytest pluggings 1/2

Performance:
- **pytest-profile**
- pytest-durations
- pytest-perf
- pytest-timeout: Set timeout on tests

Environment:
- **pytest-env**: Handle environment
- **pytest-logger**: Handle logger

---

# Pytest pluggings 2/2

Tech:
- pytest-mongodb
- pytest-postgresql
- pytest-django

Others:
- **pytest-xdist**: parallelization over multiple CPUs
- pytest-mock: wrapper over unittest.mock

---
# Plugin highlights
### pytest-profile

Profile your tests:
- Find slow functions
- Useful to find missing mocks!
- A bit too verbose at times

`pytest tests.py --profile`

---
# Plugin Highlights
### pytest-env

Set env vars in `pyproject.toml`
No need to use fixtures for that

```toml
#pyproject.toml
[tool.pytest_env]
HOME = "~/tmp"
TRANS_RIGHTS = "true"
CATS = "amazing"
```

---
# Plugin Highlights
### pytest-logger

Control logging in your tests:
- Split app logging and test logging
- Control log level to troubleshoot mocks/fixtures
- Log to stdout or files

---
# Pluging Highlights
### Pytest Xdist

Splits tests across multiple CPUs to speed up execution.
- Very useful for slow tests (integration tests with sleeps).
- Watch out for unexpected side effects.
- If you're concerned about your test speed, there are other places to look first.

---

# Misc.

Other nice things to keep in mind:
- parametrize
- monkeypatch
- logassert
- mocking and imports
- exitstack

---

# Misc - Parametrize

Run the same test with multiple different parameters:
```python
@pytest.mark.parametrize("test_input, expected", [(1, 2), (2, 4), (3, 6)])
def test_double(test_input, expected):
    assert test_input * 2 == expected
```

```
=================== test session starts ===================
...
collected 3 items
examples/ex_04/misc_tests.py ...                    [100%]
==================== 3 passed in 0.01s ====================
```

---

# Misc - Monkeypatch

Kinda like a mock, but "dirtier".
- Useful for mocking attributes/environment of existing objects
- Guaranteed to undo/teardown on test end

```python
def test_env(monkeypatch):
    assert os.getenv("BEST_SINGER") is None

    monkeypatch.setenv("BEST_SINGER", "Hatsune Miku")
    assert os.getenv("BEST_SINGER") == "Hatsune Miku"

    monkeypatch.setenv("BEST_SINGER", "Tracy Chapman")
    assert os.getenv("BEST_SINGER") == "Tracy Chapman"
```

---

# Misc - caplog

Builtin fixture to capture logs
- access logs with `caplog.records`
- access text with `caplog.text`

```python
def test_log_assert(caplog):
    logger.warning("Hey Link!")
    assert "Link" in caplog.text
```

If you're trying to mock loggers, use this instead!

--- 

# Misc - Mocking and imports (1/2)

This does not work!
```python
#main.py
import foo
foo()  # <- This function call is executed on import!

def main():
   ...
```
```python
#test.py

# When python tries to find this reference, 0-indent instructions are run!
with mock.patch("main.foo"):
    ...
```

---

# Misc - Mocking and imports (2/2)

Fixing:
- Avoid runing code on import-time/0-indent
- Mock something below `foo`
- Mock the import module itself - Only use if above options are bad

This is the cause for the biggest headaches I've had so far.

---

# ExitStacks

`contextlib.ExitStack` lets you enter many context managers at the same time.

```python
@pytest.fixture
def mock_functions():
    with mock.patch("model_1") as model_1:
        with mock.patch("model_2") as model_2:
            with mock.patch("model_3") as model_3:
                yield model_1, model_2, model_3
```

```python
@pytest.fixture
def mock_functions():
    with ExitStack() as stack:
        yield [
            stack.enter_context(mock.patch("model_1")),
            stack.enter_context(mock.patch("model_2")),
            stack.enter_context(mock.patch("model_3")),
        ]
```

---

# Resources and References

- [UnitTest Docs](https://docs.python.org/3/library/unittest.html)
- [Pytest Docs](https://docs.pytest.org/en/8.0.x/index.html)
- [Pytest How-To Guides](https://docs.pytest.org/en/8.0.x/how-to/index.html#how-to)
- [Pytest Plugin List](https://docs.pytest.org/en/8.0.x/reference/plugin_list.html#plugin-list)
- [Mocks Arent's Stubs](https://martinfowler.com/articles/mocksArentStubs.html)

Slides made with [MARP](https://marp.app/), the Markdown Presentation Ecosystem.
Slides and code available on github: github.com/itxasos23/pytest_hike

---

# Q&A

---

# Python, a short hike


### PyBCN 🐍 2024/02/21


_Itxaso (Txas) Aizpurua_

txas@txas.me - github.com/itxasos23 
itxasos@blahaj.social

