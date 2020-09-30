# project-eddy
<br>
<h2>Extraction daily insights from water consumption</h2>

The idea of this work is to try and extract daily insights about per household water consumption whilst not yet having smart meters.
The way we do it here is by looking at each day individually as an aggregate of all meter readings that include that day and assume that is suggestive of what the consumption for that day is in general compared to other days, and also whether for some of the different types of households that trend is different.

Here is an illustration of the idea - the inputs to the model for that day are all the meter readings that cross over that day: <br>

![Daily Insights Concept](/images/daily_insight_concept.png)

Here is an example of one of the resulting distribution for one of the customers, after applying the series of daily models - rather than a series of flat lines we now have daily variance, which arguably is a step in the right direction: <br>

![Daily Meter Read Variance](/images/daily_meterread_variance.png)

A good way to progress this work is to install sufficient number of smart meters to be able to validate the daily variance and then use the insights to map onto the rest of the network and have a really useful PCC / Marketing solution. Meter read data is often partial, having one or two reads over many years for a large portion of the customers, and there are often data quality issues, for example date or reading entered wrong that now plays tricks on our model.

<h3> Performance </h3>

You can expect to get the following performance on the final model: <br>

Training set score: 82% <br>
Testing set score: 77%

<h3> Modelling technique </h3>

We use xgboost regression throughout.

<h3> Process </h3>

* Featurisation <br>
  -Aggregate average weather figures across the reading window
  -Use the dummy variable approach to categoricals
  -Apply exclusions
* Build daily variance models <br>
  -Select modelling window <br>
  -Create a model for each day of the modelling window
* Redistribute daily consumption figures according to the daily models' insight <br>
  -Run daily model predicton on the values for the day rather than aggregates over the meter read window <br>
  -Preserve total consumption figures per meter read window
* Generate final daily dataset <br>
  -Take samples from the data in order to fit into memory <br>
  -Ensure preservation of more of the COVID data as it is scarcer <br>
  -Add seasonality and COVID19 variables <br>
  -Add persisting weather trends variables
* Build general daily model <br>
  -Ensure we split the data by customer rather than by day to get fair train vs. test insights <br>
  -Hide previous consumption data from the model at this point in order to learn to separate data under COVID influence better
* Redistribute daily consumption yet again during the COVID19 window <br>
  -Take away COVID's impact as we can't afford to exclude most of 2020 data from our model <br>
  -Estimate percentage impact of COVID19
* Build final model <br>
  -Add all previous consumption variables to increase our accuracy <br>
  -Take away all COVID-related variables <br>
  -Produce model validation
  
<h3>Data</h3>

Note: Data is anonymised. Use some or all of the data to build a model or create your own dataset by using your own networks' data. <br>

* Meter readings <br>
  -Includes domestic vs nondomestic <br>
  -Includes measured vs Unmeasured
* Household descriptive data <br>
  -Class description <br>
  -Misc descriptions <br>
  -Building class <br>
  -Building age <br>
  -Building type <br>
  -Storeys
* Acorn demographics data <br>
  -Category, groupy and type <br>
  -Occupancy rate
* Weather data - median daily AW-wide values per weather variable <br>
  -Air Pressure <br>
  -Compass <br>
  -Humidity <br>
  -Lightning Count <br>
  -Radiation <br>
  -Rainfall <br>
  -Rainfall Intensity <br>
  -Temperature <br>
  -Wind Chill <br>
  -Wind Direction <br>
  -Wind Speed <br>
* Seasonality <br>
  -Month of the year <br>
  -Day of the week <br>
  -School holidays <br>
  -Public holidays <br>
  -COVID period <br>
  -COVID stage <br>
  -New COVID deaths <br>
  -New Hospital admissions <br>
  -New COVID cases
  
<h3>Why is this useful?</h3>

* Know to-date per capita consumption figures across the board
* Run various what-if scenarios. Any scenario-related data that a company anticipates to use must be included into the model. Alternatively the model can be quickly re-trained to include new types of data
* Improve marketing campaigns and their targetting
* This model can still be used at meter read windows level to predict what the next / current meter reading would look like, then we can fully validate it with 80-90% accuracy reading by reading, and overall PHC / PCC figures that vary <1% compared to actuals
* The daily models can be skipped and the general and final model can use the standard 'daily_consumption' as dependent variable rather than the redistributed 'new_daily_consumption' if it feels like we are doing too much data manipulation here.

<h3>Next steps</h3>

* Source smart meter data and map insights to existing network by using clustering (acorn types, property variables and so on) or simple mapping onto acorn types for example.
* Install smart meters in one representative DMA for insight as well as validation
* Share ideas among water companies and propose changes / improvements to this model

<h3>Requirements</h3>

* 256GB Memory
* 12-24+ hours running time depending on the number of cores used, we used 32
* Jupyter Notebook - see requirements.txt for libraries used. Use 'pip install -r requirements.txt' to install the libraries.

<h3>Any questions?</h3>

Please post them here and we'll do our best to answer them.
