import factory.random
import pytest
from freezegun import freeze_time


@pytest.fixture(autouse=True)
def setup_test_environment():
    factory.random.reseed_random("777")
    with freeze_time("2020-01-04"):
        yield
