"""Backend part of the weather application."""
import sqlite3
import csv
import sys
import os
from datetime import date

data_file = "data.csv"
dic = {"timeArgument": ["2020-01-01", "2020-01-02"],
       "timeIntervallType": "TIME_INTERVALL", "Argument": "nederbordsmangd"}


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
        attribute_id = insert_values_to_attribute_table("Attributes", data, c)
        insert_values_to_datapoints_table("Datapoints", data, c, attribute_id)
        return "File uploaded succesfully!"
    else:
        return data
    close_db(db)


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
    sql_get_id = """SELECT ID, Unit FROM Attributes WHERE Name = '""" + \
        filters["Argument"]+"""'"""
    data = c.execute(sql_get_id)
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
        sql_get_data = """SELECT * FROM Datapoints WHERE Year BETWEEN '"""+str(start_date[0])+"""'AND '"""+str(end_date[0])+"""' AND Month BETWEEN '"""+str(
            start_date[1])+"""' AND '"""+str(end_date[1])+"""' AND Day BETWEEN '"""+str(start_date[2])+"""' AND '"""+str(end_date[2])+"""' AND AttributeID = """+str(attr_id)+""";"""
        datapoints_to_return = c.execute(sql_get_data)
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
        sql_get_data = """SELECT * FROM Datapoints WHERE Month = '""" + \
            str(month)+"""' AND AttributeID = '"""+str(attr_id)+"""';"""
        datapoints_to_return = c.execute(sql_get_data)
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


def insert_values_to_datapoints_table(table, data, c, attribute_id):
    """Seperate string of data into comma seperated values.
    and add to datapoint table.
    """
    date_index = 0
    for row in data:
        if len(row) != 0 and row[0] == "Datum" and row[1] == "Tid (UTC)":
            date_index = data.index(row)
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
        return db
    except sqlite3.Error as error:
        raise Exception


def close_db(db):
    """Close database connection."""
    db.close()


def initialize_table(db, c):
    """Create table."""
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
    c.execute("""PRAGMA foreign_keys = ON;""")
    attributes_table = c.execute(sql_create_attributes_table)
    datapoints_table = c.execute(sql_create_datapoints_table)
    db.commit()
    list_of_values = file_reader(data_file)
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
