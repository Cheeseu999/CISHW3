# CIS4340 HW3
**Write up for Homework 3**

## Introduction
The purpose of this assignment is to data scrape the Wikipedia page of the SpaceX Falcon 9/Heavy Launches, and create nine small reports using that data. 
This will be done once with Beautiful Soup and once with ScrapeGraphAI in a Python extraction program. The code was written and ran in Anaconda's Spyder IDE.
<br>

## Beautiful Soup
For the non-AI web scrapers, there were two options: Beautiful Soup and Scrapy. I decided to go with Beautiful Soup simply because, unlike Scrapy, I had already heard of it before this assignment.
<br><br>
The webscraping portion of the extraction code references this [helpful article](https://www.datahen.com/blog/web-scraping-using-python-beautiful-soup/), which guides on how to use
Beautiful Soup on Wikipedia. 
<br><br>
The actual extraction is quite simple, the Wikipedia page is grabbed by inputting its URL in requests. Then the page is put through Beautiful Soup, parsing the content as HTML.
The tables of the HTML (which is what we are concerned with) are pulled out and then formatted into pandas dataframes. One dataframe for each table.

```python
# get wikipedia page 
 url = "https://en.wikipedia.org/wiki/List_of_Falcon_9_first-stage_boosters" 
  
 try: 
     page = requests.get(url) 
 except Exception as e: 
     print('Error downloading page: ', e) 
      
      
 # create html soup of the page and grab all table sections 
 soup = BeautifulSoup(page.text) 
 tables = soup.find_all('table') 
  
 # create pandas data frame for each table 
 dfs = [] 
 for table in tables: 
     dfs.append(pd.read_html(str(table))[0]) 
```
Thankfully, the Wikipedia tables are translated into pandas dataframes with little trouble. The rest (and admittedly largest) part of the work concerns cleaning each table and
unifying the formatting of all the tables, so that a single cumulative table can be outputted as a CSV.
<br>
Each table is: 

- renamed
- drops unneeded columns and rows
- adds new columns (flight_type, total_launches, etc.)
- cleans strings in current columns
- converts dates into proper YYY-MM-DD format.
- reordered so columns align between tables

The code shows an example of cleaning Table 1. This process is repeated for all four tables we will be using.

```python
 # Clean up table 1 
 B1 = dfs[0].copy(deep = True) 
  
 # clean up table to follow hw format 
 B1 = B1.rename(columns={'S/N[a]': 'engine_number', 'Flight No.[b]': 'flight_number', 'Launch date (UTC)[6]' : 'launch_date', 
                    'Launch (pad)' : 'launch_pad', 'Landing' : 'landing_location', 'Fate' : 'engine_status', 'Version' : 'block_type'}) 
  
 # drop uneeded columns and rows 
 B1.drop(columns=['Payload[c]'], inplace = True) 
 B1.drop([25], inplace = True) 
  
 # create flight type and turnaround time columns and add to table 
 flight_type = [] 
 for i in range(len(B1)):  
     flight_type.append(B1.iloc[i].flight_number[:2]) 
 B1.insert(4, 'flight_type', flight_type) 
 B1.insert(7, 'turnaround_time', 0) 
 B1.insert(9, 'total_launches', 1) 
  
 # convert version to block type and remove brackets for engine_status 
 for i in range(len(B1)):  
     B1.loc[i, 'block_type'] = B1.iloc[i].block_type[1:4] 
  
     # check if engine_status has brackets and remove if they do 
     if(B1.iloc[i].engine_status[-1] == ']'): 
         size = len(B1.iloc[i].engine_status) - 4 
         B1.loc[i, 'engine_status'] = B1.iloc[i].engine_status[:size] 
  
  
 # convert dates to proper format 
 for i in range(len(B1)): 
     try: 
         B1.loc[i, 'launch_date'] = datetime.strptime(B1.loc[i, 'launch_date'], "%d %B %Y").strftime("%Y-%m-%d") 
     except: 
         B1.loc[i, 'launch_date'] = 'N/A'
```

Finally, once the dataframes are all cleaned, they are concatenated together and outputted as a 'Blocks.csv' file using pandas'
to_csv() function, separated by commas.

```python
 # combine all three data frames 
 df = pd.concat([B1, B4, B5, B5_2], ignore_index=True) 
  
 # clean all '-' entries 
 df = df.replace('—', 'N/A') 
 df = df.replace('‑', '‑') 
  
 # convert to csv 
 df.to_csv('Blocks.csv', index=False, sep=',')
```

Overall, the actual scraping part was quick to write and run. Cleaning took a bit longer, but the file is now ready to be used in the reports.

## ScrapeGraphAI
While using BeautifulSoup was a straightforward process, the same can't be said for the AI web scraper ScrapeGraphAI. The way ScrapeGraphAI works is that the model is given a url and a prompt, written out by the user. Since the prompt can be anything within reason, it allows for much more flexible information retrieval. At the same time, however, this flexibility makes it so that getting the exact information you need in the way you want it can be difficult.

To create the extraction program, I this time wrote in Jupyter, as it would take multiple attempts to scrape the website, so the cell block format of Jupyter helped a lot with organization. I also used LangChain to get the API keys I needed to run ScrapeGraphAI.

### Attempt 1
One benefit of using LangChain beyond getting an API Key, is that they allow you to create an output schema for your prompt, meaning you can curate exactly what you need the output to look like. I wanted to see if I could use this output schema to get the data essentially pre-formatted and pre-cleaned all into one table. 

The output schema and prompt are as follows:
```python
class F9_Tables(BaseModel):
    engine_number: List[str] = Field(description="The tables column labelled S/N. Values begin with B and then a list of numbers. There will be repeat engine numbers.")
    block_type: List[str] = Field(description="The tables column labelled 'Version' or 'Type'")
    launch_date: List[str] = Field(description="The tables column labelled something like 'Launch Date', contain dates as [day month year]")
    flight_number: List[str] = Field(description="The tables column labelled something like 'Flight No.' and contains strings like 'F#-###'")
    launch_pad: List[str] = Field(description="The tables column labelled something like 'Launch (pad)', talks about sucess and failures")
    landing_location: List[str] = Field(description="The tables column labelled something like 'Landing'")
    engine_status: List[str] = Field(description="The tables column labelled something like 'Fate' or 'Status'")
    turnaround_time: List[str] = Field(description="The tables column labelled something like 'Turnaround time', if a table doesn't have this output or column autofill a value of zero")


# SmartScraper request
response = sgai_client.smartscraper(
    website_url="https://en.wikipedia.org/wiki/List_of_Falcon_9_first-stage_boosters",
    user_prompt="Extract the four tables from the Wikipedia website page that lists different Falcon 9 launches. There is one table in 'v1.0 and v1.1', one table in 'Full Thrust up to Block 4', and two tables in 'Block 5'. There should be about 500 overall launches to record, and some launches will have repeat engine_numbers, list the repeats too.",
    output_schema=F9_Tables
)
```
I made sure to only add columns necessary for the output schema, and specified a base value of 0 for turnaround time, as I knew the Block 1.0 and 1.1 graphs would not have that column. With the prompt, I tried to detail which four tables the AI needed to scrape. I also mentioned the repeating engine numbers, as I had guessed there may be a possibility that the AI would skip rows that shared the same engine number.
<br><br>
Unfortunately, while the output was clean and neat as I had wanted, it notably only resulted in grabbing 55 of the roughly 500 total rows. It also still skipped rows despite me warning about it in the prompt.
After trying a few more attempts, modifying the wording of the output schema and prompt each time, the same problem would remain. It seemed the output schema might not be viable for this assignment.

### Attempt 2
I decided that since the more strict prompting wasn't working, that I would try again without an output schema but the same prompt.

```python
# SmartScraper request
response = sgai_client.smartscraper(
    website_url="https://en.wikipedia.org/wiki/List_of_Falcon_9_first-stage_boosters",
    user_prompt="Extract the four tables from the Wikipedia website page that lists different Falcon 9 launches. There is one table in 'v1.0 and v1.1', one table in 'Full Thrust up to Block 4', and two tables in 'Block 5'. There should be about 500 overall launches to record, and some launches will have repeat engine_numbers, list the repeats too.",
)
```
This time, more rows were found! While much better, it still didn't catch all the rows of all the tables. Additionally, an issue quickly cropped up that each of the four tables had different column names, and which row came from which table was not clear. This means that cleaning up this output would be a major headache. Therefore, I decided to try one more attempt.

### Attempt 3
For my final attempt, I once again removed the output schema, but specified in the prompt to output each table in a separate group. The prompt was as follows:
```python
# SmartScraper request
response = sgai_client.smartscraper(
    website_url="https://en.wikipedia.org/wiki/List_of_Falcon_9_first-stage_boosters",
    user_prompt="Extract the four tables from the Wikipedia website page that lists different Falcon 9 launches. There is one table in 'v1.0 and v1.1', one table in 'Full Thrust up to Block 4', and two tables in 'Block 5'. There should be about 500 overall launches to record, and some launches will have repeat engine_numbers, list the repeats too. Please separate the output for each table.",
)
```
The AI did listen and output each table individually. The good news: the first two tables had all their rows scraped! The bad news: the third and fourth tables had only a few of their rows. At this point, I was a bit stuck with the AI Scraper, and I had run out of free key usages on two different LangChain accounts. So, for this assignment, I am leaving the AI output incomplete. I converted each dictionary list outputted by the AI into pandas dataframes. I cleaned and formatted the incomplete tables the same way I did with beautifulsoup, then I outputted the combined AI scraped data by using pandas' to_csv() function. 
<br><br>
Overall, it seems that the headache of using an AI webscraper, as it is in its current form, may not be worth it. This is especially the case for structured data that already has non-AI alternatives that work quickly and easily. 

## Reports
Writing the programs for each report was mostly simple. Converting the csv to a pandas dataframe allows easy manipulation of the data to get what is needed, and most of the programs only needed a simple sorting of a column for filtering of rows based on a condition or two. The only issues were that for sorting the data, it would sometimes need to be converted into other data types (as they are all string columns).

```python
numbers = (df_both['turnaround_time']).str[:-5].astype(float)
numbers = numbers.rename('time')
df_both = pd.concat([df_both, numbers], axis = 1)

df_both = df_both.sort_values(by='time', ascending=[True])
df_both = df_both.drop(columns=['time'])
```
*For the program longestTurnaround, the table needed to be sorted by the days in the turnaround_time column*

There was also the problem that the data contained symbols that didn't have a one-to-one conversion for the txt file out, meaning that I had to convert the dataframe to string and then enocde it as "utf-8". 

```python
with open('mostLaunches.txt', 'w', encoding="utf-8") as f:
    print(df_both.to_string(index=False), file = f)
```
Otherwise, the rest of the programs ran without difficulty and text files were successfully created for each program.

