# Database

For the database, sqlite3 is used. The database file is named weather_data.db and is located in the `instance` folder. When a file is imported into the program, all its data is stored in the database. It should be assured that no duplicate data is stored. New data takes precedence over existing data. 

## Connecting

For each transaction of queries to the database, a new connection should be established and closed once the transaction is completed.

Example code:
```python
def get_db():
    db = sqlite3.connect(
        'weather_data.db',
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row

    return db


def close_db(db):
    db.close()
```

## Database tables
| Datapoints |             |
| ---------- | ----------- |
| PK         | ID          |
|            | Year        |
|            | Month       |
|            | Day         |
|            | Time        |
|            | Value       |
| FK         | AttributeID |


| Attributes |      |
| ---------- | ---- |
| PK         | ID   |
|            | Name |
|            | Unit |

# Datafile

All uploaded datafiles should follow the following format specification:
* All files are presented in a csv-file with `;` as the separator and uses `.` for the decimal seperator.
* The table should have the following layout:
   - The following should exist somewhere in the file:
      | +                 | Enhet         |
      | ----------------- |
      | Name of unit      |
      | +                 | Parameternamn |
      | ----------------  |
      | Name of parameter |
    - The list of the main data should be formatted in the following way:
        | Datum                         | Tid (UTC)                     | Parameternamn                        | Other columns (Will be ignored) |
        | ----------------------------- | ----------------------------- | ------------------------------------ | ------------------------------- |
        | Date given in ISO-8601 format | Time given as HH:MM:SS in UTC | Value for the parameter without unit | Other data that will be ignored |
        | ...                           | ...                           | ...                                  | ...                             |
    - Other data presented in the file will be ignored.
* All data should be mesured in metric units.

# Program structure

* All data from the database is stored in a list of dictionaries.
* Each method is responsible for opening and closing the database connection using the helper methods provided.
* The program should be written in an imperative and/or functional paradigm.
* Follow the development guidelines for codestyle and testing.
* The backend program should work as an interface and filter between the database and frontend program. 