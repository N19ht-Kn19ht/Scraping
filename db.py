import psycopg2

from config import host, user, password, db_name


def connect():
    try:
        # Connect to exist db
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        connection.autocommit = True

        # Create the cursor object
        cursor = connection.cursor()

        return connection, cursor

    except Exception as ex:

        return print("[INFO] Error while working with PostgreSQL", ex)


def insert_data(link, title, price_usd, mileage, name, phone, image_url, count_images, car_number, car_vin,
                datetime):

    con = connect()

    connection = con[0]
    cursor = con[1]

    # Create a table
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS cars(
                id SERIAL PRIMARY KEY,
                link VARCHAR NOT NULL,
                title VARCHAR NOT NULL,
                price_usd INTEGER NOT NULL,
                mileage INTEGER,
                name VARCHAR(50),
                phone BIGINTEGER,
                image_url VARCHAR NOT NULL,
                count_images INTEGER NOT NULL,
                car_number VARCHAR,
                car_vin VARCHAR,
                datetime TIMESTAMP NOT NULL);"""
    )
    print("[INFO] Table created successfully")

    # Insert data into a table
    insert = """INSERT INTO cars (link, title, price_usd, mileage, name, phone, image_url, count_images,
    car_number, car_vin, datetime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

    data = (link, title, price_usd, mileage, name, phone, image_url, count_images, car_number, car_vin, datetime)

    cursor.execute(insert, data)

    print("[INFO] Data was successfully inserted")

    # print(f"Server version: {cursor.fetchone()}")

    return close_connect(connection, cursor)


def close_connect(connection, cursor):
    if connection:
        cursor.close()
        connection.close()
        print("[INFO] PostgreSQL connection closed")
    return

