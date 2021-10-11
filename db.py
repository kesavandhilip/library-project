#!/usr/bin/python
import sqlite3

def connect_to_db():
    conn = sqlite3.connect('store.db')
    return conn

def create_library_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE libraries (
                library_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                postal_code TEXT NOT NULL
            );
        ''')

        conn.commit()
        print("libraries table created successfully")
    except:
        print("libraries table creation failed - Maybe table")
    finally:
        conn.close()

def create_book_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE books (
                book_id INTEGER PRIMARY KEY NOT NULL,
                title TEXT NOT NULL,
                author_name TEXT NOT NULL,
                isbn_num TEXT NOT NULL,
                genre TEXT NOT NULL,
                description TEXT NOT NULL
            );
        ''')

        conn.commit()
        print("books table created successfully")
    except:
        print("books table creation failed - Maybe table")
    finally:
        conn.close()

def create_library_books_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE library_books (
                library_book_id INTEGER PRIMARY KEY NOT NULL,
                library_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                last_library_activity_id INTEGER NOT NULL,
                FOREIGN KEY(library_id) REFERENCES libraries(library_id),
                FOREIGN KEY(book_id) REFERENCES books(book_id)
            );
        ''')

        conn.commit()
        print("library books table created successfully")
    except:
        print("library books table creation failed - Maybe table")
    finally:
        conn.close()

def create_users_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL
            );
        ''')

        conn.commit()
        print("users table created successfully")
    except:
        print("users table creation failed - Maybe table")
    finally:
        conn.close()

def create_library_activities_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE library_activities (
                library_activity_id INTEGER PRIMARY KEY NOT NULL,
                activity_type TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                library_book_id INTEGER NOT NULL,
                checked_out_at TEXT,
                checked_in_at TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            );
        ''')

        conn.commit()
        print("library activities table created successfully")
    except:
        print("library activities table creation failed - Maybe table")
    finally:
        conn.close()