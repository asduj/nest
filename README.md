nest
====

Installation
------------
```bash
$ pip install -r requirements.txt
```

If you use `poetry` or any other modern dependency packaging tool you can install
packages using `pyproject.toml`:

```bash
$ poetry install
```

Tests
-----
Tests are located under `tests` folder. To run it use `pytest`:

```bash
$ pytest
```

Console usage
-------------
```bash
$ python -m nest.py nesting_level_1 nesting_level_2 ... nesting_level_n
```

JSON data reads from stdin after required levels:

```bash
$ cat tests/fixtures/input.json | python -m nest currency country city
```

It could be done manually by ending input with `control + D`:

```bash
$ python -m nest currency
[{"country": "US", "city": "Boston", "currency": "USD"}]
{
    "USD": [
        {
            "country": "US",
            "city": "Boston"
        }
    ]
}

```

For better display, you can adjust the number of spaces to indent:
```bash
$ python -m nest currency country city --indent 4
```

API usage
---------
Run server with `uvicorn` for instance:
```bash
$ uvicorn server:app
```

Code for API endpoint is located in the file `server.py`.

Server provide the only single API endpoint `/nest`.

This the API can only be used by the admin.

Keys for nesting should be placed in params and input data sends as POST json body.
```bash
$ curl "http://127.0.0.1:8000/nest/?keys=currency&keys=country&keys=city" \
-X POST \
--user admin:admin \
-H "Content-Type: application/json" \
-d @tests/fixtures/input.json
```
 
