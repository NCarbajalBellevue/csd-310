import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values

# Read the .env file
secrets = dotenv_values(".env")

# Database configuration
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

try:
    # Connect to the database
    db = mysql.connector.connect(**config)

    # Create cursor
    cursor = db.cursor()

    # Query 1 - Studio table
    print("-- DISPLAYING Studio RECORDS --")

    cursor.execute("SELECT studio_id, studio_name FROM studio")

    studios = cursor.fetchall()

    for studio in studios:
        print("Studio ID:", studio[0])
        print("Studio Name:", studio[1])
        print()

    # Query 2 - Genre table
    print("-- DISPLAYING Genre RECORDS --")

    cursor.execute("SELECT genre_id, genre_name FROM genre")

    genres = cursor.fetchall()

    for genre in genres:
        print("Genre ID:", genre[0])
        print("Genre Name:", genre[1])
        print()

    # Query 3 - Films under 2 hours
    print("-- DISPLAYING Short Film RECORDS --")

    cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120")

    films = cursor.fetchall()

    for film in films:
        print("Film Name:", film[0])
        print("Runtime:", film[1])
        print()

    # Query 4 - Films ordered by director
    print("-- DISPLAYING Director RECORDS in Order --")

    cursor.execute("SELECT film_name, film_director FROM film ORDER BY film_director")

    directors = cursor.fetchall()

    for director in directors:
        print("Film Name:", director[0])
        print("Director:", director[1])
        print()

except mysql.connector.Error as err:

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")

    else:
        print(err)

finally:
    if "cursor" in locals():
        cursor.close()

    if "db" in locals() and db.is_connected():
        db.close()