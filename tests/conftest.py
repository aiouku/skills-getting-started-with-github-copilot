import copy
import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client():
    """Provide a TestClient and reset `app_module.activities` after each test."""
    backup = copy.deepcopy(app_module.activities)
    with TestClient(app_module.app) as c:
        yield c

    # restore the original activities to avoid test coupling
    app_module.activities.clear()
    app_module.activities.update(backup)
