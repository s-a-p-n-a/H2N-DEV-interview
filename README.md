
# XML Processing, JSON Conversion, and Data Handling in Python




## description
This task involves processing XML files by converting them to JSON format and storing both the raw XML and processed JSON data in an SQLite database. The script includes error handling for missing elements, malformed structures, or unexpected fields. Retrying failed operations up to 3 times. Additionally, unit tests validate the XML parsing and logging functionality to ensure robustness.
## Approach
1. Understand the requirement of the task
2. Followed the steps and work on them accordingly
3. Planned the work flow:
i) Download the XML files from zip and stored in a folder name xml-files

ii) Imported xml.etree.ElementTree and json to perform feild extraction i.e OrderID, Customer, and Products and converts the extracted data into json.

iii) Imported os, logging and datetime for process log and Implement error handling using try-except-finally to ensure that files continue processing even after failures and retries attempt up 3 time.

iv) Performed the bonus task by importing sqlite3 and created database orders.db to store raw as well as processed data.

v) For unit testing created a new python file unit_test_xml.py using import unittest.
## Challenges and solution approach 
1. XML files has missing or improperly closed tags, leading to ParseError exceptions.
To solve this error used except for error handling, missing elements.

2. Error log 
ensure that script should not crash or fail to run for that implemented retry mechanism to run script completely without terminating.

3. writing unit test faced type error 
for this Double-checked that the function call match the function and corrected it.


## Tools and resources used
Python

VS Code

GitHub

ChatGPT 

YouTube
