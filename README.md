# BGSU Faculty Collaboration Website 
## Overview
Our team has been asked to create a web application to help facilitate collaboration in research between BGSU faculty members and assist in finding grants quickly. To do this faculty members will be able to sign in and search keywords for upcoming projects and our algorithms will search faculty CVs and other relevant data with the keyword(s) to retrieve relevant faculty. We will also supply a link to the SPIN Grant website to help find grants.

## How To Run
1. Create SQL database
2. Enter database login info in 'Backend Prototype/backendPrototype/backendPrototype/settings.py'
3. In the 'Backend Prototype/backendPrototype' directory, run this command in command line: ```python manage.py migrate```
    * This creates the tables in the database
4. Next we need to populate the tables, modify this file with the your directory where CV's are stored, this outputs a csv that is read in step 5
    * 'CV processing/research_interests_extract.py'
5. Run the ```populate_database()``` function in 'Backend Prototype/backendPrototype/dbConnector/views.py', this populates the database based on the csv from step 4
6. Run ```python manage.py runserver``` to start the server 

## Current Progress
### Sprint 1
- Have a basic UI prototype with everything necessary to function. It has been designed to look similar with other BGSU sites.
- Designing the database layout using MySQL and planning how we will store our data before we begin writing algorithms for the text mining. 
- Setup the basic Django environment for accessing the database and reading and writing data to a local database
### Sprint 2
- Have polished off the Figma prototype with a more appealing design and interactiveness.
- Built the first HTML/CSS templates for the Home and Results page.
- Finished a simplified version of CV Data extraction
- Figured out how to insert extracted CV data into Django database
- Implemented the HTML/CSS templates in Django with very basic functionality
### Sprint 3
- Cleaned up CSS for better scalability on verious devices
- Improved button functionality on the various webpages
- Implemented the search function to return results from the database based on the user's search query.
### Sprint 4
- Added update button to nav bar.
- Made template for updating information (will be implemented later).
- Fixed basic spelling/wording that customer wanted changed.
- Updated logic for returning interests and names from database.
### Sprint 5
- Formatted and connected update page.
- Formatted results to look cleaner and add dynamic data for department.
- Added data to our database of different faculty.
- Added intro paragraph to home page expalinging the website.

### Sprint 6
- Changed wording, titling and some spacing.
- Transitioned our dev environemnt from our local windows machine to a linux VM.

## Sprint 7
- Added dropdown menu for searching.
- Made results page and update page more readable.
- Added backend functionality for dropdown.
- Added functionality for the update page to now be able to upload CVs from the website and store it in the database.

## Sprint 8
- Added login button.
- Formatted search bar.
- BGSU logo now takes links to homepage.

## Sprint 9
- In the process of adding a dropdown section for publications to the results page.
- Formatted some titling.
- CVs when uploaded will now be scrapped and their data will be presented for corrections by the user before uploading to the database.
- When searching using the radial menu the selected search type is now displayed at the top of the results.

## Sprint 10
- Implemented a login with django that is a proof of concept for the sso
- Added more tables to the database for storing faculty information.

## Sprint 11
- Allow user to change data without uploading new facilitate
- Made research interests into a list in results
- Added collapsibles for publications and grants
- Updated login page to match the rest of the website

## Sprint 12
- Corrected a bug causing some searchs to return incorrect data
- Added pop-up box to show success or failure when uploading CVs

# Next Steps
- Implement sso
- Improve search funcionality to a machine learning approach which finds research interests related to the search string
    - Example: Searching for Machine Learning should also bring up Neural Networks
- Query BGSU's faculty database directly when trying to find validate a persons name, instead of using our lookup tables
    - This assures the most up to date data is used
