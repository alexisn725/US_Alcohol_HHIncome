# US Alcohol Sales and Household Income
## Code Kentucky Data 2


### Data Set 1 - Median Household Income by State

This project uses a data set provided by the US government as part of the Current Population Survey with the *US Census Bureau*. The link to the table I used can be found here: 

(https://www.census.gov/data/tables/time-series/demo/income-poverty/historical-income-households.html)

I used the data table **Table H-8. Median Household Income by State** for this project, but there are several more tables that break down the findings of the Current Population Survey that are pretty interesting if you're keen to find more statistics on Median Household Income in the USA. 

### Data Set 2 - Alcohol Sales by State

This project also uses a data set provided by the US government as part of their Surveillance Reports from the *National Institute on Alcohol Abuse and Alcoholism.* The link can be found here:  

https://pubs.niaaa.nih.gov/publications/surveillance-covid-19/COVSALES.htm

The data set provided was used to create the Surveillance Report: **Alcohol Sales During the COVID-19 Pandemic** and contains per capita alcohol sales between the years of 2017 - 2021 of beer, wine, and spirits during the Covid-19 pandemic for 13 states so far. The NIAAA also created several charts of their own on the data; if you're interested in viewing more I would definitely take a look. 

# Summary:
My aim was to combine these two datasets to see if there was a correlation within the states between median household income and alcohol sales, during the Covid pandemic years. 

For both data sets, I downloaded the .xlsx data file provided by the researchers and converted that into a CSV file for ease. Once that was done I cleaned the data to get rid of extraneous information, and merged the two using a pandas merge. Once that was completed, I was able to analyze the data to find: 

- There is a slight negative relationship between Household Income, and Alcohol Sales.
- A positive correlation exists between Gallons and Population.
  - this suggests that more research could be done to see if per capita, the sales are equivalent without population inflating the numbers.
- A negative correlation exists between Population and Household Income.

These findings came from the calculations performed on the merged dataframe and were shown using matplotlib and Tableau visualizations. 

### Data Dictionary

| Column Name   | Description      | Data Type  |
| ------------- |:-------------:| -----:|
| Year          | calendar year, between 2019 and 2021 | Object |
| Month  | calendar month, in digit form from 1-12      | Int64 |
| State| geographical location in USA     |  Object |
| Beverage | Type of alcoholic beverage: spirits, wine, beer| Object
| Gallons | amount of gallons of beverages sold | Int64
| Population | US population recorded, 14+ | Int64
| HHIncome | Median household income per state, from Census Bureau | Int64


This project was completed by mostly using Jupyter Notebook, but US_Alcohol_HHIncome.ipynb or US_Alcohol_HHIncome.py should work with any editor. 

The required modules to run this data file is included in the requirements.txt file. Once the github repo has been cloned, it should be fairly easy to run and use the file. 

## Requirement 1: Read Data In
- For both datasets, the .xlsx files were downloaded separately as a local CSV file, and read into a pandas dataframe.

## Requirement 2: Clean, Combine, Analyze Data
- The datasets were separately cleaned of extra columns and rows, making sure everything was uniform. A inner join pandas merge was used to join the two datasets into one merged dataframe. 
- Analysis was then done with the addition of some new calculations, such as finding: 
  - total gallons of alcohol sold per state, per year
  - average median household income per state
  - correlation of alcohol sold and income
  amongst other things
  

## Requirement 3: Visualize Data
- 3 Tableau charts were created, and then put into a Tableau dashboard to display
- 1 seaborn chart was created 

## Requirement 4: Best Practices
- A data dictionary was created that describes the columns of the final merged dataset. It is above in the Readme.

## Requirement 5: Interpretation
- Code was annotated using Markdown cells in Jupyter notebook, as well as clear code comments. 

Thank you for viewing!
