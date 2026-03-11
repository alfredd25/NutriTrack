import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_redis():
    redis = MagicMock()
    redis.get.return_value = None
    redis.setex.return_value = True
    redis.delete.return_value = True
    return redis
