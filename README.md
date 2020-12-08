# 206-final-project
Instructions on how to run the code

1- Open up the zipped file. Make sure the only things in the project folder are files that end in “.py”, the README, the pdf of the Report, and the two folders 'calculations' and 'visualizations', both of which should be empty before beginning to run the code. The only files needed to start running the code are the python files. There should be no database, images, csv files, or anything else not mentioned above in the folder. Make sure they are deleted if they are in there before running the code.

2- Make sure anaconda is fully installed on your computer. This will ensure that python is fully up to date as well as matplotlib. Also, make sure SQLite Database Browser Portable is installed so that you can view the database once you create it. The API and website do not need to be installed before running the code.

3- Run the file “final.py”. This should be run 7-8 times. It may take a while each time you run it because a lot of data is being extracted every time. You will know everything is finished running once all 5 graphs have come up on your screen and the correlations have been displayed in the terminal. When you begin running the code, it will create a database called “finalProjectDatabase.db” and will create the tables “Temperatures”, “WeatherData", “HappyData”, and “LatLongData” within the database. You will now be able to see the finalProjectDatabase.db file in the project folder. With SQLite Database Browser Portable installed, you will be able to view the tables within the database. At the end, there should be 182 rows in all of the tables except the Temperatures table. This one will only have 168 rows. 

4- Next, the “cal_vis.py” file will run automatically once all of the data has been collected from the “final.py” file. This file will be called in the last run of "final.py".The “calc_vis.py” file will do the calculations from the data in the database and create the visualizations for the calculations. The calculations will all be saved within the 'calculations' folder in the project folder. The visualizations will all be saved within the 'visualizations' folder in the project folder. You can view the calculations in the csv files within the 'calculations' folder after everything is done running. They will be titled “tempHappy.csv” for the temperature vs. happiness scores data, “precipHappy.csv” for the precipitation vs. happiness scores data, “temp.csv” for the temperature boxplot data, “precip.csv” for the precipitation boxplot data, and “happy.csv” for the happiness scores boxplot data. You can view the visualizations in the png files within the 'visualizations' folder after everything is done running as well. The visualizations will be labelled “tempHappyScatterplot.png”, “precipHappyScatterplot.png”, “tempBoxplot.png”, “precipBoxplot.png”, and “happyBoxplot.png” corresponding to the data in the png files respectively. Plus, when in the 7th run of the project, each visualization will display on your screen once you get to it in the code. You must close out of the image in order to allow the file to continue to run. Once the file is finished running, you will have all of these images and csv files in the folders in the overall project folder and the code will also output the correlation coefficients for the first two visualizations within the terminal. 

5- In the end, you can now open finalProjectDatabase.db, any of the csv files, and any of the png images to view the database tables, calculations, and visualizations.
