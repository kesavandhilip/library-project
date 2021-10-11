from db import connect_to_db, create_library_table
import sqlite3
from datetime import datetime

def insert_library(library):
    inserted_library = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO libraries (name, city, state, postal_code) VALUES (?, ?, ?, ?)", (library['name'], library['city'], library['state'], library['postal_code']) )
        conn.commit()
        inserted_library = get_library_by_id(cur.lastrowid)
    except:
        conn().rollback()

    finally:
        conn.close()
    return inserted_library

def get_library_by_id(library_id):
    library = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM libraries WHERE library_id = ?", (library_id,))
        row = cur.fetchone()
        
        library["library_id"] = row["library_id"]
        library["name"] = row["name"]
        library["city"] = row["city"]
        library["state"] = row["state"]
        library["postal_code"] = row["postal_code"]
    except Exception as e:
        library = {}
    return library

def insert_book(book):
    inserted_book = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO books (title, author_name, isbn_num, genre, description) VALUES (?, ?, ?, ?, ?)", (book['title'], book['author_name'], book['isbn_num'], book['genre'], book['description']) )
        conn.commit()
        inserted_book = get_book_by_id(cur.lastrowid)
    except:
        conn().rollback()

    finally:
        conn.close()
    return inserted_book


def get_book_by_id(book_id):
    book = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
        row = cur.fetchone()

        book["book_id"] = row["book_id"]
        book["title"] = row["title"]
        book["author_name"] = row["author_name"]
        book["isbn_num"] = row["isbn_num"]
        book["genre"] = row["genre"]
        book["description"] = row["description"]
    except Exception as e:
        book = {}
    return book

def insert_user(user):
    inserted_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name) VALUES (?)", (user['name'],))
        conn.commit()
        inserted_user = get_user_by_id(cur.lastrowid)
    except:
        conn().rollback()

    finally:
        conn.close()
    return inserted_user


def get_user_by_id(user_id):
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()

        user["user_id"] = row["user_id"]
        user["name"] = row["name"]
    except Exception as e:
        user = {}
    return user

def create_checkin_book(checkin_data):
    user = {}
    book = {}
    result = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        #validate user
        cur.execute("SELECT * FROM users WHERE name = ?", (checkin_data["name"],))
        row = cur.fetchone()
        user["user_id"] = row["user_id"]
        if user["user_id"] == "":
            result["messageStatusCode"] = "1400"
            result["messageStatusDescription"] = "Requested user is not avilable"
            return result
        
        #validate book
        cur.execute("SELECT * FROM books WHERE title = ?", (checkin_data["title"],))
        row = cur.fetchone()
        book["book_id"] = row["book_id"]
        if book["book_id"] == "":
            result["messageStatusCode"] = "1400"
            result["messageStatusDescription"] = "Requested book is not avilable"
            return result

        if user["user_id"] != "" and book["book_id"] !="":
            now = datetime.now()
            cur.execute("INSERT INTO library_activities (activity_type, user_id, library_book_id, checked_out_at, checked_in_at) VALUES (?, ?, ?, ?, ?)", (checkin_data["access_type"], user["user_id"], 1, "", now) )    
            library_activity_id = cur.lastrowid
            conn.commit()
            cur.execute("INSERT INTO library_books (library_id, book_id, last_library_activity_id) VALUES (?, ?, ?)", (1, book["book_id"], cur.lastrowid) )
            sql = ''' UPDATE library_activities
              SET library_book_id = ?
              WHERE library_activity_id = ?'''
            cur.execute(sql, (cur.lastrowid, library_activity_id))
            result["messageStatusCode"] = "2000"
            result["messageStatusDescription"] = "Successfully checkin the user"
            return result
    except Exception as e:
        print(e)
        result = {}
    return result

def create_checkout_book(checkout_data):
    user = {}
    library = {}
    book = {}
    result = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        #validate user
        cur.execute("SELECT * FROM users WHERE name = ?", (checkout_data["name"],))
        row = cur.fetchone()
        user["user_id"] = row["user_id"]
        if user["user_id"] == "":
            result["messageStatusCode"] = "1400"
            result["messageStatusDescription"] = "Requested user is not avilable"
            return result
        
        #validate book
        cur.execute("SELECT * FROM books WHERE title = ?", (checkout_data["title"],))
        row = cur.fetchone()
        book["book_id"] = row["book_id"]
        if book["book_id"] == "":
            result["messageStatusCode"] = "1400"
            result["messageStatusDescription"] = "Requested book is not avilable"
            return result

        if user["user_id"] != "" and book["book_id"] !="":
            now = datetime.now()
            cur.execute("INSERT INTO library_activities (activity_type, user_id, library_book_id, checked_out_at, checked_in_at) VALUES (?, ?, ?, ?, ?)", (checkout_data["access_type"], user["user_id"], 1, str(now), "") )    
            library_activity_id = cur.lastrowid
            cur.execute("SELECT * FROM libraries WHERE library_id = ?", (11,))
            library_row = cur.fetchone()
            library["library_id"] = library_row["library_id"]
            cur.execute("INSERT INTO library_books (library_id, book_id, last_library_activity_id) VALUES (?, ?, ?)", (library["library_id"], book["book_id"], library_activity_id) )
            library_books_id = cur.lastrowid
            sql = ''' UPDATE library_activities
              SET library_book_id = ?
              WHERE library_activity_id = ?'''
            cur.execute(sql, (library_books_id, library_activity_id))
            result["messageStatusCode"] = "2000"
            result["messageStatusDescription"] = "Successfully checkout the user"
            return result
    except Exception as e:
        print(e)
        result = {}
    return result

def list_of_checkout_book_by_id(userdetail):
    result = {}
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        #validate user
        cur.execute("SELECT * FROM users WHERE name = ?", (userdetail,))
        row = cur.fetchone()
        user["user_id"] = row["user_id"]
        if user["user_id"] == "":
            result["messageStatusCode"] = "1400"
            result["messageStatusDescription"] = "Requested user is not avilable"
            return result
        #validate library_activities
        cur.execute("SELECT * FROM library_activities WHERE user_id = ? and activity_type = ?", (user["user_id"], 'checkout',))
        rows = cur.fetchall()
        checkedout_book_list = []
        for i in rows:
            book = {}
            book["name"] = userdetail
            book["checked_out_at"] = i["checked_out_at"]
            cur.execute("SELECT * FROM library_books WHERE library_book_id = ?", (i["library_book_id"],))
            library_book_row = cur.fetchone()
            if library_book_row != "":
                cur.execute("SELECT * FROM libraries WHERE library_id = ?", (library_book_row["library_id"],))
                library_row = cur.fetchone()
                book["library_name"] = library_row["name"]
                cur.execute("SELECT * FROM books WHERE book_id = ?", (library_book_row["book_id"],))
                book_row = cur.fetchone()
                book["book_name"] = book_row["title"]
            checkedout_book_list.append(book)
        return checkedout_book_list
    except Exception as e:
        print(e)
        result = {}
    return result
