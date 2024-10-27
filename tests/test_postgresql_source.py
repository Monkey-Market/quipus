import pytest
from psycopg_pool import ConnectionPool
from quipus import PostgreSQLDataSource


@pytest.fixture
def postgresql_data_source():
    """Fixture para crear una instancia de PostgreSQLDataSource con parámetros básicos."""
    return PostgreSQLDataSource(
        host="localhost",
        database="test_db",
        user="test_user",
        password="test_password",
        port=5432,
        pool_size=5,
        timeout=15,
    )


@pytest.fixture
def mocked_connection_pool(monkeypatch, postgresql_data_source):
    """Fixture para mockear el pool de conexiones y el cursor."""

    class MockCursor:
        def execute(self, query):
            pass

        def fetchall(self):
            return [(1, "test"), (2, "data")]

        @property
        def description(self):
            MockDescription = type("MockDescription", (), {"name": "id"}), type(
                "MockDescription", (), {"name": "value"}
            )
            return MockDescription

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            pass

    class MockConnection:
        def cursor(self):
            return MockCursor()

        def commit(self):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            pass

    class MockConnectionPool:
        def connection(self):
            return MockConnection()

        def close(self):
            self.closed = True

    mock_pool = MockConnectionPool()
    monkeypatch.setattr(
        postgresql_data_source, "_PostgreSQLDataSource__connection_pool", mock_pool
    )
    return postgresql_data_source, mock_pool


def test_postgresql_data_source_initialization(postgresql_data_source):
    assert postgresql_data_source.host == "localhost"
    assert postgresql_data_source.database == "test_db"
    assert postgresql_data_source.user == "test_user"
    assert postgresql_data_source.password == "test_password"
    assert postgresql_data_source.port == 5432
    assert isinstance(
        postgresql_data_source._PostgreSQLDataSource__connection_pool, ConnectionPool
    )


def test_postgresql_data_source_setter_invalid_host(postgresql_data_source):
    with pytest.raises(TypeError, match="'host' must be a string."):
        postgresql_data_source.host = 123
    with pytest.raises(ValueError, match="'host' cannot be an empty string."):
        postgresql_data_source.host = ""


def test_postgresql_data_source_invalid_port(postgresql_data_source):
    with pytest.raises(ValueError, match="'port' must be between 1 and 65535."):
        postgresql_data_source.port = 70000
    with pytest.raises(TypeError, match="'port' must be an integer."):
        postgresql_data_source.port = "5432"


def test_postgresql_data_source_empty_user(postgresql_data_source):
    with pytest.raises(ValueError, match="'user' cannot be an empty string."):
        postgresql_data_source.user = ""
    with pytest.raises(TypeError, match="'user' must be a string."):
        postgresql_data_source.user = 123


def test_postgresql_data_source_empty_password(postgresql_data_source):
    with pytest.raises(ValueError, match="'password' cannot be an empty string."):
        postgresql_data_source.password = ""

    with pytest.raises(TypeError, match="'password' must be a string."):
        postgresql_data_source.password = 123


def test_postgresql_data_source_fetch_data(mocked_connection_pool):
    postgresql_data_source, _ = mocked_connection_pool
    data, columns = postgresql_data_source.fetch_data("SELECT * FROM test_table")

    assert data == [(1, "test"), (2, "data")]
    assert columns == ["id", "value"]


def test_postgresql_data_source_execute_query(mocked_connection_pool):
    postgresql_data_source, _ = mocked_connection_pool
    postgresql_data_source.execute_query(
        "INSERT INTO test_table (id, value) VALUES (1, 'test')"
    )

    conn = postgresql_data_source._PostgreSQLDataSource__connection_pool.connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO test_table (id, value) VALUES (1, 'test')")
    conn.commit()


def test_postgresql_data_source_close_pool(mocked_connection_pool):
    postgresql_data_source, mock_pool = mocked_connection_pool
    postgresql_data_source.close_pool()
    assert getattr(
        mock_pool, "closed", False
    ), "El pool de conexiones debería estar cerrado."


def test_postgresql_data_source_str(postgresql_data_source):
    expected_str = "PostgreSQLDataSource(host=localhost, port=5432, database=test_db, user=test_user)"
    assert str(postgresql_data_source) == expected_str
