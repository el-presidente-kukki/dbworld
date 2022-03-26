import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv

load_dotenv()

conn = None
try:
    # Connect to an existing database
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(user=os.getenv('DB_USERNAME'),
                            password=os.getenv('DB_PASSWORD'),
                            host=os.getenv('DB_HOST'),
                            port=os.getenv('DB_PORT'),
                            database=os.getenv('DB_DATABASE'))
    # create a cursor
    cur = conn.cursor()

    # execute a statement
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')

    # display the PostgreSQL database server version
    db_version = cur.fetchone()
    print(db_version)
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        print('Database connection working like a charm.')


def disconnectdb():
    conn.close


def insert_allmails(df):
    print("Write all to MailDatasetTable")
    query = "INSERT INTO maildatasettable(date_received, from_name, from_mail, subject, body) values(%s,%s,%s,%s,%s);"
    for i in range(len(df)):
        """ Execute a single INSERT request """
        try:
            cur.execute(query, (
                df.loc[i, "Date_Received"], df.loc[i, "From_Name"], df.loc[i, "From_Mail"], df.loc[i, "Subject"],
                df.loc[i, "Body"]))
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            conn.rollback()
            cur.close()
            return 1
        print(df.loc[i, "Subject"] + " was written to the DB")


def insert_mail(date_received, from_name, from_mail, subject, body):
    """print("Insert Single Mail")"""
    query = "INSERT INTO maildatasettable (date_received, from_name, from_mail, subject, body) values(%s,%s,%s,%s,%s) RETURNING id;"

    """ Execute a single INSERT request and return ID """
    try:
        cur.execute(query, (date_received, from_name, from_mail, subject, body))
        conn.commit()
        id_of_new_row = cur.fetchone()[0]

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()
        return 1
    return id_of_new_row + 1


def insert_singlekeyword(keywords, mail_id):
    """print("Insert Keywords to ID: ", mail_id)"""
    query = "INSERT INTO keywordssingle(id, keyword) values(%s, %s)"

    for index, tuple in enumerate(keywords):
        """ Execute a single INSERT request """
        '''print('Insert Keyword:'+ tuple[0])'''
        try:
            cur.execute(query, (mail_id, tuple[0]))
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            conn.rollback()
            cur.close()
            return 1


def insert_multiplekeyword(keywords, mail_id):
    """print("Insert Keywords to ID: ", mail_id)"""
    query = "INSERT INTO keywordsmultiple(id, keyword) values(%s, %s)"
    for index, tuple in enumerate(keywords):
        """ Execute a single INSERT request """
        '''print('Insert Keyword:'+tuple[0])'''
        try:
            cur.execute(query, (mail_id, tuple[0]))
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            conn.rollback()
            cur.close()
            return 1


def keybert_test(keywords, mail_id):
    # print("Insert Keyword:" + keywords + " to ID:" + mail_id)
    query = "INSERT INTO keywordssingle(id, keyword) values(%s, %s)"
    print(keywords)
    print(type(keywords))

    for index, tuple in enumerate(keywords):
        print(tuple[0])


def get_byname(name):
    print("Get Mails by Name:")