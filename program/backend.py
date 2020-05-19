"""Backend part of the weather application."""
import sqlite3
import csv
import sys
import os
import flask

data_file = "data.csv"


def file_reader(data_file):
    """Open CSV file and appends data to a list."""
    with open(data_file, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')

        data = []
        for row in reader:
            data.append(row)
        return data


def process_file(file):
    """Insert valeus from uploaded file."""
    check = ext_check(file)
    db = access_db()
    c = db.cursor()
    if type(check) is list:
        attribute_id = insert_values_to_attribute_table("Attributes", check, c)
        insert_values_to_datapoints_table("Datapoints", check, c, attribute_id)
        return "File uploaded succesfully!"
    else:
        return check
    close_db(db)


def get_attributes():
    """Get attributes from table."""
    db = access_db()
    c = db.cursor()
    sqlite_get_data = """SELECT Name, DisplayName FROM Attributes;"""
    attr_data = c.execute(sqlite_get_data)
    data_to_return = {}
    for row in attr_data:
        data_to_return["Name"] = row[0]
        data_to_return["DisplayName"] = row[1]
    close_db(db)
    return data_to_return


def get_data(filters):
    db = access_db()
    c = db.cursor()


def ext_check(file):
    """Check if extension is csv."""
    ext = os.path.splitext(file)
    if ext[1] == '.csv':
        return file_reader(file)
    else:
        return "File is not in the correct format"


def insert_values_to_datapoints_table(table, data, c, attribute_id):
    """Seperate string of data into comma seperated values.
    and add to datapoint table.
    """
    date_index = 0
    for row in data:
        if len(row) != 0 and row[0] == "Datum" and row[1] == "Tid (UTC)":
            date_index = data.index(row)
        else:
            return "Some expected data does not exist"
    for row in range((date_index + 1), len(data)):
        values_to_add = ""
        sql_insert = """ INSERT INTO """+table+"""
        (Year, Month, Day, Time, Value, AttributeID)
        VALUES ("""
        for i in data[row][0]:
            if i == "-":
                sql_insert += ","
            else:
                sql_insert += i
        sql_insert += ","
        for i in range(1, 3):
            if i == 1:
                for i in data[row][1]:
                    if i != ":":
                        sql_insert += i
                    else:
                        break
            else:
                sql_insert += data[row][i]
            if i != 2:
                sql_insert += ","
        sql_insert += ","
        sql_insert += str(attribute_id)
        sql_insert += ");"
        c.execute(sql_insert)
    # print(sql_insert)


def insert_values_to_attribute_table(table, data, c):
    """Check for special characters and replace with english alphabet
    (if necessary) and add to datapoint table."""
    parameter_index_column = 0
    attribute_index_column = 0
    parameter_index_row = 0
    attribute_index_row = 0
    string_to_add = ""
    for row in data:
        if len(row) != 0 and "Parameternamn" in row:
            parameter_index_column = row.index("Parameternamn")
            parameter_index_row = data.index(row)
    for row in data:
        if len(row) != 0 and "Enhet" in row:
            attribute_index_column = row.index("Enhet")
            attribute_index_row = data.index(row)
    sql_insert = """ INSERT INTO """+table+"""(Name, DisplayName, Unit)
        VALUES ("""
    for i in data[parameter_index_row + 1][parameter_index_column]:
        if i == "Ä" or i == "ä" or i == "Å" or i == "å":
            string_to_add += "a"
        elif i == "Ö" or i == "ö":
            string_to_add += "o"
        else:
            string_to_add += i
    string_to_add = string_to_add.lower()
    sql_insert += ('"' + string_to_add + '"' + ',')
    sql_insert += ('"'+data[parameter_index_row + 1]
                   [parameter_index_column] + '"' + ',')
    sql_insert += ('"' + data[attribute_index_row + 1]
                   [attribute_index_column]+'"')
    sql_insert += ");"
    c.execute(sql_insert)
    return c.lastrowid


def access_db():
    """Retrieve database."""
    try:
        db = sqlite3.connect(
            'instance\\weather_data.db',
            detect_types=sqlite3.PARSE_DECLTYPES

        )
        db.row_factory = sqlite3.Row
        print("Created and connected to database successfully.")
        return db
    except sqlite3.Error as error:
        print("Error while retriving database", error)


def close_db(db):
    """Close database connection."""
    db.close()
    print("Successfully closed connection")


def create_table(db, create_table_sql, c):
    """Insert data into database."""
    try:
        c.execute(create_table_sql)
    except sqlite3.Error as error:
        print(error)


def initialize_table(db, c):
    """Create table."""
    sql_create_datapoints_table = """CREATE TABLE IF NOT EXISTS Datapoints (
        ID integer PRIMARY KEY,
        Year integer,
        Month integer,
        Day integer,
        Time text,
        Value real,
        AttributeID integer);"""
    sql_create_attributes_table = """CREATE TABLE IF NOT EXISTS Attributes(
        ID integer PRIMARY KEY,
        Name text,
        DisplayName text,
        Unit text
        );"""
    c.execute("""PRAGMA foreign_keys = ON;""")
    attributes_table = create_table(db, sql_create_attributes_table, c)
    datapoints_table = create_table(db, sql_create_datapoints_table, c)
    db.commit()
    add_data_to_tables(attributes_table, datapoints_table, c, db)


def add_data_to_tables(attributes_table, datapoints_table, c, db):
    """Add data to tables."""
    list_of_values = ext_check(data_file)
    attribute_id = insert_values_to_attribute_table(
        "Attributes", list_of_values, c)
    insert_values_to_datapoints_table(
        "Datapoints", list_of_values, c, attribute_id)
    db.commit()
    close_db(db)


def initiate_database():
    """Initialize database if it does not exist, otherwise creates it."""
    db = access_db()
    c = db.cursor()
    initialize_table(db, c)


if __name__ == '__main__':
    globals()[sys.argv[1]]()
