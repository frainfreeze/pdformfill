# pdformfill

Fill PDF forms by generating FDF data and then using [`pdftk`](http://www.pdflabs.com/tools/pdftk-server/) to push the fdf into a PDF form and generate the output.

## Quick install

    pip install pdformfill

## How to use
If our form had fields "name" and "telephone" we would fill it as follows:

```python
#!/usr/bin/env python3
import pdformfill

fields = [('name', 'John Smith'), ('telephone', '555-1234')]
pdformfill.fill_pdf(fields, "input.pdf", "output.pdf")
```

## Running tests
* Create a virtual environment
* tox is required to run the tests. You can install the correct version with
  `pip install -r requirements-tests.txt`
* Run `tox` to run tests for all Python versions.
* To run a specific test and specific Python versions, you may use `tox -e py37
  -- tests/test_encoding.py`