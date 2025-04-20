# CIS4340 HW3
**Write up for Homework 3**

### Introduction
The purpose of this assignment is to data scrape the Wikipedia page of the SpaceX Falcon 9/Heavy Launches, and create nine small reports using that data. 
This will be done once with Beautiful Soup and once with ScrapeGraphAI in a Python extraction program.
<br>

### Beautiful Soup
For the non-AI web scrapers, there were two options: Beautiful Soup and Scrapy. I decided to go with Beautiful Soup simply because, unlike Scrapy, I had already heard of it before this assignment.
<br><br>
The webscraping portion of the extraction code references this [helpful article](https://www.datahen.com/blog/web-scraping-using-python-beautiful-soup/), which guides on how to use
Beautiful Soup on Wikipedia. 
<br><br>
The actual extraction is quite simple, the Wikipedia page is grabbed by inputting its URL in requests. Then the page is put through Beautiful Soup, parsing the content as HTML.
The tables of the HTML (which is what we are concerned with) are pulled out and then formatted into pandas dataframes. One dataframe for each table.
https://github.com/Cheeseu999/CISHW3/blob/1d2057cc4711fa7592b763f996c78b35414d00f0/f9Extract.py#L14-L30
<br>
Thankfully, the Wikipedia tables are translated into pandas dataframes with little trouble. The rest (and admittedly largest) part of the work concerns cleaning each table and
unifying the formatting of all the tables, so that a single cumulative table can be outputted as a CSV.
<br>
Each table is: 
* renamed
* drops unneeded columns and rows
* adds new columns (flight_type, total_launches, etc.)
* cleans strings in current columns
* converts dates into proper YYY-MM-DD format.
* reordered so columns align between tables
<br>
The code shows an example of cleaning Table 1. This process is repeated for all four tables we will be using.
https://github.com/Cheeseu999/CISHW3/blob/1d2057cc4711fa7592b763f996c78b35414d00f0/f9Extract.py#L33-L67

<br>
Finally, once the dataframes are all cleaned, they are concatenated together and outputted as a 'Blocks.csv' file using pandas'
to_csv() function, separated by commas.
https://github.com/Cheeseu999/CISHW3/blob/1d2057cc4711fa7592b763f996c78b35414d00f0/f9Extract.py#L217-L225




