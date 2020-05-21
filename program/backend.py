"""Backend part of the weather application."""
import sqlite3
import csv
import sys
import os
import datetime
import unidecode


data_file = "data.csv"


def file_reader(data_file):
    """Open CSV file and appends data to a list."""
    ext = ext_check(data_file)
    if ext:
        with open(data_file, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            data = []
            for row in reader:
                data.append(row)
            return data
    elif not ext:
        return "File is not in the correct format"


def ext_check(file):
    """Check if extension is csv."""
    ext = os.path.splitext(file)
    if ext[1] == '.csv':
        return True
    else:
        return False


def process_file(file):
    """Insert values from uploaded file."""
    data = file_reader(file)
    db = access_db()
    c = db.cursor()
    if type(data) is list:
        attribute_id = insert_values_to_attribute_table(data, c)
        insert_values_to_datapoints_table(data, c, attribute_id)
        close_db(db)
        return "File uploaded succesfully!"
    else:
        close_db(db)
        return data


def get_attributes():
    """Get attributes from table."""
    db = access_db()
    c = db.cursor()
    sqlite_get_data = """SELECT Name, DisplayName FROM Attributes;"""
    attr_data = c.execute(sqlite_get_data)
    data_to_return = []
    for row in attr_data:
        data_to_return.append({"name": row[0], "displayName": row[1]})
    close_db(db)
    return data_to_return


def get_data(filters):
    """Get data from databases using filters."""
    db = access_db()
    c = db.cursor()
    data = c.execute("SELECT ID, Unit FROM Attributes WHERE Name = ?", (filters["Argument"],))
    for bit in data:
        attr_id = bit[0]
        unit = bit[1]
    dates = filters["timeArgument"]
    if filters["timeIntervallType"] == "TIME_INTERVALL":
        start_date = dates[0]
        start_date = start_date.split("-")
        start_date[1] = int(start_date[1])
        start_date[2] = int(start_date[2])
        end_date = dates[1]
        end_date = end_date.split("-")
        end_date[1] = int(end_date[1])
        end_date[2] = int(end_date[2])
        sql_get_data = "SELECT * FROM Datapoints WHERE Year BETWEEN ? AND ? AND Month BETWEEN ? AND ? AND Day BETWEEN ? AND ? AND AttributeID = ?;"
        datapoints_to_return = c.execute(sql_get_data, (str(start_date[0]), str(end_date[0]), str(
            start_date[1]), str(end_date[1]), str(start_date[2]), str(end_date[2]), str(attr_id)))
        data_to_return = []
        for data in datapoints_to_return:
            data_to_return.append({"id": data[0],
                                   "year": data[1],
                                   "month": data[2],
                                   "day": data[3],
                                   "time": data[4],
                                   "value": data[5],
                                   "unit": unit
                                   })
        close_db(db)
        return data_to_return
    elif filters["timeIntervallType"] == "MONTH":
        month = dates[0]
        month = int(month)
        sql_get_data = "SELECT * FROM Datapoints WHERE Month = ? AND AttributeID = ?;"
        datapoints_to_return = c.execute(
            sql_get_data, (str(month), str(attr_id)))
        data_to_return = []
        for data in datapoints_to_return:
            data_to_return.append({"id": data[0],
                                   "year": data[1],
                                   "month": data[2],
                                   "day": data[3],
                                   "time": data[4],
                                   "value": data[5],
                                   "unit": unit
                                   })
        close_db(db)
        return data_to_return
    close_db(db)


def insert_values_to_datapoints_table(data, c, attribute_id):
    """Seperate string of data into comma seperated values.
    and add to datapoint table.
    """
    date_index = 0
    for row in data:
        if len(row) != 0 and row[0] == "Datum" and row[1] == "Tid (UTC)":
            date_index = data.index(row)
    for row in range((date_index + 1), len(data)):
        date = datetime.datetime.fromisoformat(data[row][0])
        time = datetime.datetime.strptime(data[row][1], '%H:%M:%S')
        sql_insert = "INSERT INTO Datapoints(Year, Month, Day, Time, Value, AttributeID) VALUES ( ?, ?, ?, ?, ?, ?)"
        c.execute(sql_insert, (date.year, date.month, date.day, time.hour, data[row][2], str(attribute_id)))


def insert_values_to_attribute_table(data, c):
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
    sql_insert = " INSERT INTO Attributes (Name, DisplayName, Unit) VALUES ( ?, ?, ?)"
    c.execute(sql_insert, (unidecode.unidecode(data[parameter_index_row + 1][parameter_index_column]).lower(), data[parameter_index_row + 1][parameter_index_column], data[attribute_index_row + 1][attribute_index_column]))
    return c.lastrowid


def access_db():
    """Retrieve database."""
    try:
        db = sqlite3.connect(
            'instance\\weather_data.db',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        db.row_factory = sqlite3.Row
        return db
    except sqlite3.Error as error:
        raise Exception


def close_db(db):
    """Close database connection."""
    db.close()


def initialize_database():
    """Creates database (if it does not exist)."""
    sql_create_datapoints_table = """CREATE TABLE IF NOT EXISTS Datapoints (
        ID integer PRIMARY KEY,
        Year text,
        Month text,
        Day text,
        Time text,
        Value real,
        AttributeID integer);"""
    sql_create_attributes_table = """CREATE TABLE IF NOT EXISTS Attributes(
        ID integer PRIMARY KEY,
        Name text,
        DisplayName text,
        Unit text
        );"""
    db = access_db()
    c = db.cursor()
    c.execute("PRAGMA foreign_keys = ON;")
    attributes_table = c.execute(sql_create_attributes_table)
    datapoints_table = c.execute(sql_create_datapoints_table)
    db.commit()
    list_of_values = file_reader(data_file)
    attribute_id = insert_values_to_attribute_table(list_of_values, c)
    insert_values_to_datapoints_table(list_of_values, c, attribute_id)
    db.commit()
    close_db(db)


if __name__ == '__main__':
    globals()[sys.argv[1]]()