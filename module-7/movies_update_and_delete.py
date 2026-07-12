# Name: Natalia Carbajal
# Date: 7/12/2026
# Assignment: Module 7.2
# Purpose: Insert, update, and delete records from the movies database.

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


# Function to display the films
def show_films(cursor, title):

    print(f"\n-- {title} --")

    query = """
        SELECT film_name AS Name,
               film_director AS Director,
               genre_name AS Genre,
               studio_name AS Studio
        FROM film
        INNER JOIN genre ON film.genre_id = genre.genre_id
        INNER JOIN studio ON film.studio_id = studio.studio_id
        ORDER BY film_id
    """

    cursor.execute(query)

    for film in cursor.fetchall():
        print("Film Name:", film[0])
        print("Director:", film[1])
        print("Genre:", film[2])
        print("Studio:", film[3])
        print()


try:
    # Connect to the database
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    # Display current films
    show_films(cursor, "DISPLAYING FILMS")

    # Insert a new film
    cursor.execute("""
        INSERT INTO film
        (film_name, film_releaseDate, film_runtime, film_director, genre_id, studio_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, ("Inception",2010, 148,"Christopher Nolan",2,1))

    db.commit()
    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    # Update Alien to Horror
    cursor.execute("""
        UPDATE film
        SET genre_id = 1
        WHERE film_name = 'Alien'
    """)

    db.commit()
    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE")

    # Delete Gladiator
    cursor.execute("""
        DELETE FROM film
        WHERE film_name = 'Gladiator'
    """)

    db.commit()
    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")


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