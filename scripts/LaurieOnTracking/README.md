# LaurieOnTracking
Laurie's code for reading and working with Metrica's tracking and event data.

The sample data can be found in Metrica's github repository here: https://github.com/metrica-sports/sample-data

We'll be updating this repo as the friends of tracking series develops, adding code for measuring player velocity and acceleration, measuring team formations, and evaluating pitch control using a model published by Will Spearman. 

To create movies from the tracking data you'll need to have ffmpeg installed. You can do this by following the instructions here: https://anaconda.org/conda-forge/ffmpeg (you may need to restart python afterwards).


Tutorial Synopsis
-----------------

Tutorial1: https://www.youtube.com/watch?v=8TrleFklEsE

An introduction to working with Metrica Sport's player tracking and event data. Options for visualising the data, and using tracking data to add context to shot maps and passing maps.

Tutorial2: https://www.youtube.com/watch?v=VX3T-4lB2o0

Using tracking data to add further context to football analytics. This tutorial covers: making movies from the data, measuring player velocities, and creating physical summary reports for players.


Tutorial3: https://www.youtube.com/watch?v=5X1cSehLg6s

Building your own pitch control model in python and using it to evaluate a player's passing options. Pitch control measures the probability that a team will retain possession of the ball if they pass it to another location on the field. It can be used to evaluate passing options for a player, and quantify the probability of success.

Tutorial4: https://www.youtube.com/watch?v=KXSLKwADXKI

Measuring the quality of player decision-making and valuing their actions. This tutorial introduces the concept of expected possession value (EPV), describes how to use EPV to quantify the value of passes, and demonstrates how you can combine EPV with pitch control to identify the best passing options available to the player on the ball. [The tutorial 4 script also describes other small changes to the codebase].