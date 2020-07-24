import os
import json
import pytest

import demography as dm


FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")


@pytest.fixture(scope="module")
def oac_dataset():
    """Sample postcode-to-oac11 mapping."""
    # note that in the originating ONS data, some OAC fields are not populated,
    # these are removed.
    dataset = json.load(open(os.path.join(FIXTURE_DIR, "oac.sample.json")))
    dataset = {k: v for k, v in dataset.items() if str(v) != "nan"}
    return dataset


@pytest.fixture(scope="module")
def groups_dataset():
    """The ONS OAC code to groups mapping."""

    return json.load(open(os.path.join(FIXTURE_DIR, "oacg.sample.json")))


def test_oac_mapping(oac_dataset: dict):
    post_codes = list(oac_dataset.keys())
    oac_codes = list(oac_dataset.values())
    mapped = [dm.get(post) for post in post_codes]
    assert all([_ == mapped[i] for i, _ in enumerate(oac_codes)])


def test_groups_mapping(oac_dataset: dict, groups_dataset: dict):
    post_codes = list(oac_dataset.keys())

    mapped = {post: dm.get(post, using="groups") for post in post_codes}

    assert all(
        [
            all([_ in groups_dataset[oac_dataset[k]]] for _ in v)
            for k, v in mapped.items()
        ]
    )
