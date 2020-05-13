"""Backend part of the weather application."""
import sqlite3
import csv
import sys

data_file = "data.csv"


def file_reader(data_file):
    """Open CSV file and appends data to a list."""
    with open(data_file, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')

        data = []
        for row in reader:
            data.append(row)
        return data


def insert_values_to_datapoints_table(table, data, c):
    """Seperate string of data into comma seperated values
    and add to datapoint table."""
    date_index = 0
    for row in data:
        if len(row) != 0 and row[0] == "Datum":
            date_index = data.index(row)
    for row in range((date_index + 1), len(data)):
        values_to_add = ""
        sql_insert = """ INSERT INTO """+table+"""
        (Year, Month, Day, Time, Value)
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
        sql_insert += ");"
        c.execute(sql_insert)


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


def run():
    """Run the code. """
    sql_create_datapoints_table = """CREATE TABLE IF NOT EXISTS Datapoints (
        id integer PRIMARY KEY,
        Year integer,
        Month integer,
        Day integer,
        Time text,
        Value real,
        AttributeID integer,
        FOREIGN KEY(AttributeID) REFERENCES Attributes(id));"""
    sql_create_attributes_table = """ CREATE TABLE IF NOT EXISTS Attributes(
        id integer PRIMARY KEY,
        Name text,
        DisplayName text,
        Unit text
        );"""
    db = access_db()
    c = db.cursor()
    c.execute("""PRAGMA foreign_keys = ON;""")
    attributes_table = create_table(db, sql_create_attributes_table, c)
    datapoints_table = create_table(db, sql_create_datapoints_table, c)
    db.commit()
    list_of_values = file_reader(data_file)
    insert_values_to_datapoints_table("Datapoints", list_of_values, c)
    insert_values_to_attribute_table("Attributes", list_of_values, c)
    db.commit()
    close_db(db)


if __name__ == '__main__':
    globals()[sys.argv[1]]()
