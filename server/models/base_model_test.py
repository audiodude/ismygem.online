import pytest

from server.db import drop_test_db, get_test_db, get_schema_path


class BaseModelTest:

  @pytest.fixture(autouse=True)
  def db_test(self):
    db = get_test_db()
    with db.cursor() as cursor:
      with open(get_schema_path()) as f:
        cursor.execute(f.read())
    yield db

    # Clean up after
    db.close()
    drop_test_db()
    return
