# demography

This package implements a simple mechanism for quickly loading demographic data based on post codes. This is currently only implemented for the UK. It is based on data made available by the UK's Office for National Statistics (ONS). 

The data was taken from [Geoportal](https://geoportal.statistics.gov.uk/datasets).

## Getting started

You can install `demography` with:

```bash
pip install demography
```

There's only really one main function in this package, and it works like this:

```python
import demography

demography.get("SW1A 0AA", using="groups")
```

You'll get something like:

```
['Cosmopolitans', 'Aspiring and affluent', 'Highly-qualified quaternary workers']
```

These are Classification for Output Areas (OAC) _groups_ -- demographic groupings provided by ONS for specific regions. If a specific OAC group cannot be found from the full postcode, it will default to using the prefix value (i.e. area-level demographics). If this too does not return a value, it will return the value provided by the `default` parameter.  

You can also get the group codes:

```python
demography.get("SW1A 0AA", using="oac")
```

And you'd get:

```text
2D2
```

If you want to access the mappings between OAC codes and the groups together, you can use:

```python
demography.groups("uk")
```

To give:

```text
{'1A1': ['Rural residents', 'Farming communities', 'Rural workers and families'], '1A2': ['Rural residents', 'Farming communities', 'Established farming communities'] ...
```

Finally, it can be useful to have these groups encoded with:

```python
demography.get("SW1A 0AA", using="encoded_groups")
```

To give:

```text
[30, 55, 59]
```

To retrieve the encodings for this, you can use:

```python
demography.encoded_groups("uk")
```

### Validation

As an additional benefit, you can enable validation for postcodes with:

```python
demography.get("SW1A 0AA", using="encoded_groups", validate=True)
```
