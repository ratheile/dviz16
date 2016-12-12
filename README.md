Introduction
-------------
It was mentioned in the exercise that this task should be a webpage.
For that i use Flask (because its very quick to set up).

Plotting framework is plot.ly

The Screenshots (Task 1-5) and the Animation (Task 6) can be found in the images directory

Prequisites
--------------
Plotting Framework: conda install -c https://conda.anaconda.org/plotly plotly
Webserver: Flask is installed with the default anaconda packages.

How to Start
--------------
./run.sh boots up the flask webserver
http://localhost:5000/ is the app link

Data Location
--------------
Insert the data to
/static/data/HGTdata.bin
/static/data/Pf/Pf....bin
/static/data/TCf/TCf....bin


Multivariate Visualization of Temperature and Pressure
--------------------------------------------------------
For the multivar visualization i did choose a 3d representation because it is a very interactive plot, the user can orient it in a way to focus his the region of interest.

Because the 3d plot does include 3 dimensions for free, adding a 4th was simple by altering the surface color.

Now the xy grid is the location, z grid is the pressure intensity and the color indicates the temperature at the location.

The Layer (height) is fixated.


Animation
----------

Because i really liked the insight gained from the 3d plot, i did animate the 3d plot as well at 0.4 km height.

Created with imagemagick
convert -delay 20 -loop 0 *.png animated.gif
