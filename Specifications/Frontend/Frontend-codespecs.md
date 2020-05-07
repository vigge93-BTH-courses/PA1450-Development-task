# Development guidelines

## UI
We will draw pretty pretty graphs on demand using with using matplotlib( https://matplotlib.org/tutorials/introductory/usage.html#sphx-glr-tutorials-introductory-usage-py). This is trriggered by the generate graph button. This action sends a list of attributes who's checkboxes are checked to the api, which requests the data with corresponding attributes.
See desing draw for more info.

By hovering your coursor over the graph a small box containing the corresponding data points appears outside the graph. By scrolling or finger gestures you're able to zoom in on the graph and by dragging with a funger or a coursor you're able to pan over the graph :)).

# Program structure

* All data from the database is recieved in a list of dictionaries.
* The program should be written in an imperative and/or functional paradigm.
* Follow the development guidelines for codestyle and testing. 
* The front end will work as an interface for the user to interact with the back end.
