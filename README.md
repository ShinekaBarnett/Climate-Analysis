# Climate Analysis and Exploration

## Precipitation Analysis

* Design a query to retrieve the last 12 months of precipitation data.

* Select only the `date` and `prcp` values.

* Load the query results into a Pandas DataFrame and set the index to the date column.

* Sort the DataFrame values by `date`.

* Plot the results using the DataFrame `plot` method.

  ![precipitation](Images/precipitation.png)

* Use Pandas to print the summary statistics for the precipitation data.

### Station Analysis

* Design a query to calculate the total number of stations.

* Design a query to find the most active stations.

  * List the stations and observation counts in descending order.

  * Which station has the highest number of observations?

* Design a query to retrieve the last 12 months of temperature observation data (tobs).

  * Plot the results as a histogram with `bins=12`.


## Climate App

Flask API based on the Precipitation and Station Analysis.

* FLASK is used to create routes.

### Routes

* `/api/v1.0/precipitation`

* `/api/v1.0/stations`

* `/api/v1.0/tobs`

* `/api/v1.0/<start>` 

* `/api/v1.0/<start>/<end>`

### Temperature Analysis

* Function called `calc_temps` accepts a start date and end date in the format `%Y-%m-%d` and return the minimum, average, and maximum temperatures for that range of dates.

* Function `calc_temps` is used to calculate the min, avg, and max temperatures for your trip using the matching dates from the previous year (i.e., use "2017-01-01" if your trip start date was "2018-01-01").

* Bar Chart is used to plot the min, avg, and max temperature

  * Used the average temperature as the bar height.

  * Used the peak-to-peak (tmax-tmin) value as the y error bar (yerr).
