from data_sources.postgresql_data_source import PostgreSQLDataSource


def main():
    postgres_source = PostgreSQLDataSource(
        host="<HOSTNAME>",
        database="<DATABASE>",
        user="<USERNAME>",
        password="<PASSWORD>",
        port=5432,
    )

    try:
        # First query - Se crea un pool de conexiones
        query1 = "SELECT * FROM table1;"
        data1, columns1 = postgres_source.fetch_data(query1)
        print("Datos obtenidos de table1:\n")
        print(columns1)
        for row in data1:
            print(row)

        # Segunda consulta - Se reutiliza el pool de conexiones
        query2 = "SELECT * FROM table2;"
        data2, columns2 = postgres_source.fetch_data(query2)
        print("\nDatos obtenidos de table2:\n")
        print(columns2)
        for row in data2:
            print(row)

    except Exception as e:
        print(f"Ocurrió un error: {e}")

    finally:
        postgres_source.close_pool()


if __name__ == "__main__":
    main()
