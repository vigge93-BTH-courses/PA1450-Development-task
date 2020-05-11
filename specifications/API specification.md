# Data  transfers

The data that will be communicated between the front end and the back end is the following:
* Attribute filter and time filter from the front end to the back end.
* Data points from the back end to the front end.
* .csv file with historical data from the front end to the back end.
* Response from processing the file with historical data from the back end to the front end.
* Available attributes from backend to frontend.

The front end will always be the instigator to the communication.

## Attributes and time filters

The attribute and time filters will be sent to the backend in a dictionary with the following keys:
```python
{"timeArgument": [str, (str)], "timeIntervallType": IntervallType, "Argument": str}
```
where IntervallType is a Enum. IntervallType contains two different values:
* TIME_INTERVALL
* MONTH

### TIME_INTERVALL

When using the TIME_INTERVALL type, the timeArgument consists of two datetime strings formatted according to ISO 8601. The first argument is the start date and the second argument is the end date. When the user wants to view a whole year or one month of a year, the start and end dates of these periods should be sent.

### MONTH

If the user wants to view one month accros all years, only one of the timeArguments are used and this should indicate the month of interest using the ISO 8601 format.

## Data points
The datapoints from the database should be sent as a list with dictionaries with the following keys:
```python
{
    "id": int,
    "year": int,
    "month": int,
    "day": int,
    "time": int, 
    "value": float,
    "unit": str
}
```

## .CSV file
The .csv file should be uploaded to the instance folder and a method call to the backend should be made with the name of the file as a parameter. The backend will respond with a string with the status message for the processing. A new request should then be made to the back end to get any potentially new attributes.

## Get attributes available
The back end will return a list of dictionaries with the following keys:
```python
{
    "name": str,
    "displayName": str
}
```
"name" is the name that should be used when communicating with the back end and "displayName" is the name used when presenting the attribute to the user.

# Backend method names
The following methods will exist in the back end and are called from the front end:
* get_data(filters)
* process_file(filename)
* get_attributes()

The parameters and return values follow the format specified above