# Frontend Code Specifications

## UI
We will generate graphs on demand using [matplotlib](https://matplotlib.org/tutorials/introductory/usage.html#sphx-glr-tutorials-introductory-usage-py "matplotlib"). The function is triggered by the generate graph button. This will check which attribute's checkboxes are checked and send a list containing keywords to the attributes in question to the api, which requests the data with corresponding keywords.

By hovering your coursor over the graph, a box containing the data point's data appears at the cursor's location. 

By scrolling with your cursor wheel while hovering over, or by moving your fingers in oposite directions on the graph box, you're able to zoom in or out on the graph, and by dragging with a finger or clicking, holding and dragging around with a coursor over the graph you're able to pan over the graph while zoomed in.

* for grahical specs, see [Website Specs file](Specifications/Frontend/Untitled Diagram (3).png " Website Specs file").

# Datafile

All uploaded datafiles should follow the following format specification:
* All files are presented in a csv-file with `;` as the separator and uses `.` for the decimal seperator.
* The table should have the following layout:
   - The following should exist somewhere in the file:
      | Enhet        |
      | ------------ |
      | Name of unit |

      | Parameternamn     |
      | ----------------- |
      | Name of parameter |
    - The list of the main data should be formatted in the following way:
        | Datum                         | Tid (UTC)                     | Parameternamn                        | Other columns (Will be ignored) |
        | ----------------------------- | ----------------------------- | ------------------------------------ | ------------------------------- |
        | Date given in ISO-8601 format | Time given as HH:MM:SS in UTC | Value for the parameter without unit | Other data that will be ignored |
        | ...                           | ...                           | ...                                  | ...                             |
    - Other data presented in the file will be ignored.
* All data should be mesured in metric units.

# Program structure

* All data from the database is recieved in a list of dictionaries.
* The program should be written in an imperative and/or functional paradigm.
* Follow the development guidelines for codestyle and testing. 
* The front end will work as an interface for the user to interact with the back end.
