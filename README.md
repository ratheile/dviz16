Introduction
-------------
We use Flask for the website (because its very quick to set up).

Plotting framework is plot.ly and D3 (Task 4)

Rendering
------------
All data is processed live when the 'update' button is pressed.
The processing will be quicker on multicore machines.

Prequisites
--------------
Python3 > v3.3 must be installed: `conda create --name pythonthree python=3`
Then the environment must be selected: `source activate pythonthree`
Plotting Framework: `conda install -c https://conda.anaconda.org/plotly plotly`
Webserver: Flask is installed with the default anaconda packages.

How to Start
--------------
./run.sh boots up the flask webserver
http://localhost:5000/ is the app link

Data Location
--------------
The data can be fetched from the IMDB server with the sources.sh script.
This will load the following files:

 - countries.txt
 - ratings.txt
 - genres.txt
 - running-times.txt

 Warning: All files are very large and hard to process with a text editor.

Task 3
-------
Task 1-3 was solved using offline plot.ly.

Task 4
--------
We couldnt find a framework to do the word circle plotting, therefore it is implemented with D3 in and SVG container.
