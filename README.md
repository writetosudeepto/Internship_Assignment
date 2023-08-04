# Sentiment Analysis for BlackCoffer by Sudipta Das


This repository contains a Sentiment Analysis project by Sudipta Das for BlackCoffer. 
The project aims to analyze the sentiment of articles published on the 
website insights.blackcoffer.com using Natural Language Processing (NLP) techniques.


Prerequisites
Before running the Sentiment Analysis project, ensure you have the following software installed:

* Python (version 3.7 or higher)
* pip

## How to Run

1. Navigate to the project directory
   
   cd Internship_Assignment
   
2. create a python vitual env and activate it (optional)

   1. python -m venv env
   
   2. .\env\Scripts\activate.bat

3. install the required packages by running this command

   pip install -r requirements.txt

4. Navigate to spiders directory

   cd .\assignment_blackcoffer\assignment_blackcoffer\spiders\

5. Run Scrapy crawl command
   
   scrapy crawl text_spider

   After running this command go to
   'assignment_blackcoffer/assignment_blackcoffer/data/output" folder.
   there will be text_files folder with all the files with the url name and the scraped content. and ther will be a file called "output.csv" inside which the scores will be there.
