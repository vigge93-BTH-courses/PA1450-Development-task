# Frontend Code Specifications

## UI

### Graph

We will generate line charts on demand using [matplotlib](https://matplotlib.org/tutorials/introductory/usage.html#sphx-glr-tutorials-introductory-usage-py "matplotlib"). This will integrate with the webpage using [mpld3](http://mpld3.github.io/). The function is triggered by the generate graph button. This will check which attribute radiobutton is checked and send the keyword to the web server, which requests the data with corresponding keyword from the back end.

By scrolling with your cursor wheel while hovering over, or by moving your fingers in oposite directions (apart to zoom in and together to zoom out) on the graph box, you're able to zoom in or out on the graph, and by dragging with a finger or clicking, holding and dragging around with a coursor over the graph you're able to pan over the graph while zoomed in.

* For grahical specs, see [Website Specs file](https://github.com/vigge93/PA1450-Development-task/blob/master/specifications/frontend/webpage_design_example.png " Website Specs file").

### Communication

We will be using JSON to format the data between the website and frontend. The Webserver library we will use is flask. For the webpages we will use the Jinja2 templating language, which integrates well with flask. 

The data from the attribute filters on the webpage will be sent to the server via a GET request containing the JSON data for the filters. This will be sent using the JQuery library.

The date picker will be dynamiclly displayed based on the selection of the radiobuttons. If the user chooses "Year" or "Month", a dropdown with the valid selections will appear, if the user chooses "time intervall" the two calendars shown in the diagram will appear.

#### JSON request structure

{
   "timeArgument": [timeArg1, timeArg2 (optional)],
   "timeIntervallType": "MONTH/TIME_INTERVALL",
   "Argument": attributeName
}

### Datafile upload

The Upload datafile button will bring the user to a separate webpage where the user can upload a file with historical data. The page also contains a description of the file format, which can be found in the backend specification. The file is sent to the server using a form POST request and is passed on to the back end. It is the web servers responsibility to validate that the file has the .csv file ending. It is the back ends responsibility to verify that the data in the file follows the specified format. 

## Program structure

* All data from the back end is recieved in a list of dictionaries.
* The program should be written in an imperative and/or functional paradigm.
* Follow the development guidelines for codestyle and testing. 
* The front end will work as an interface for the user to interact with the back end.
