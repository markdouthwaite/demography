# demography

This package implements a simple mechanism for quickly loading demographic data based on post codes. This is currently only implemented for the UK. It is based on data made available by the UK's Office for National Statistics (ONS). 

The data was taken from [Geoportal](https://geoportal.statistics.gov.uk/datasets).

If you want to jump to seeing how this package can play with `pandas`, [see below](#playing-with-pandas).

The package comes with built-in caching, makes extensive use of hash maps (i.e. dictionaries), and should generally be pretty fast!

As well as providing mappings to `OAC11` groups (demographic codes), you can also map to lower-level groups within these codes too. See below for examples.

Hopefully it'll save you having to repeatedly find, load and transform ONS census data!

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

## Playing with pandas

You can use `demography` to encode `pandas.DataFrame` columns pretty easily too:

```python
import pandas as pd
import demography as dm

df = pd.read_csv("my-dataset.csv")

# get the encoded 'super group', 'group', 'sub group' set. 
data_gen = (dm.get(code, using="encoded_groups") for code in df["postcode"])

# build a dataframe
dm_df = pd.DataFrame(data=data_gen, columns=["super_group", "group", "sub_group"])

# horizontally concatenate the groups dataframe to your original frame.
df = pd.concat([df, dm_df], axis=1)
```

Or alternatively, if you only need `oac11` codes, you can use:

```python
df["demographic"] = df["postcode"].apply(lambda _: dm.get(_))
```

Note that you'll need to use the name of your column for `postcode`! 
