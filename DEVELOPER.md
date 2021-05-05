# BGSU Faculty Collaboration Website - Contributions
## Developers
- Brian Blakely
- Will Arthur
- Anthony Laurio
- Jacob Budd

## Project Overview
Our team has been asked to create a web application to help facilitate collaboration in research between BGSU faculty members and assist in finding grants quickly. To dod this faculty members will be able to sign in and search keywords for upcoming projects and our algorithms will search faculty CVs and other relveant data with the keyword(s) to retrieve relevant faculty. We will also supply a link to the SPIN Grant website to help find grants.

## UI Design
### Goals
- The website should be easy to learn and use, feel natural for someone from BGSU, have all necessary features, and be in line with BGSU web design guidelines.
### Methods, Practices, and Tools 
- We have begun prototyping the UI using a tool called Figma. This is a point and click to tool that lets multiple developers work at the same time.
- When we begin building the actual UI for the solution we will use HTML/CSS with a Pytthon Django backend.
- This [page](https://www.bgsu.edu/marketing-and-communications/bgsu-graphic-standards-manual/the-official-identity-colors.html) is our key source for color codes.
- This [page](https://www.bgsu.edu/marketing-and-communications/bgsu-graphic-standards-manual/web-identity-guidelines.html) is our key source for basic web design guidelines.
- This [page](https://www.bgsu.edu/marketing-and-communications/bgsu-graphic-standards-manual/how-to-obtain-the-bgsu-logo-or-signature.html) is our key resource for BGSU images and logos.

### Current Progress
- Have a figma protoype that we may or may not update
- Have templates for the Home and Results page built in HTML/CSS that will be continually improved
- Implemented the templates in Django with search functionality and most buttons on the webpages working
- We have not implemented the templates to query the database with the backend to retrieve data dynamically.
- The home button is now working.
- CSS has been updated to avoid pizels as a unit and instead use percentages and rem.
- Added Update button to nav bar to allow faculty users to update their information.
- Made a basic template where users update their information. Still needs formatted better though.
- Fixed basic spelling and wording issues customer brought up.
- Added intro paragraph to homepage.
- Formatted Results page (specifically research interests)
- Formatted update page.
- Made basic changes to wording, titling, and spacing per the Customer's request.
- Added a dropdown menu to allow user to search for memebr, interest, or department.
- Formatted results to look nicer.
- Added a login button in the navbar for when we get that going.
- Formatted the search button. Although it is still in consistent for some reason.
- Added a homepage link to the BGSU logo on each homepage.
- Have been working on implementing a drop down section for publicaions in the results sections. Have not gotten it fully working gor the repo.
- Changed some titling to describe what the user is searching for.
- Research interests are now in a list
- Added collapsibles for publications and grants
- Updated login page to match website theme

## Text Mining

### Goals
- Extract relevant information from a CV then store it for easy processing

### Methods, Practices, and Tools 

- We will use Python for all CV data extraction scripting
- The following packages will get used for data extraction
    - PDFMiner: for extracting raw text from the pdf file
    - Spacy: for natural language processing (NLP)
    - Pandas: for local data storage and vectorization

### Current Progress
- Implemented research interests data extraction from a CV
- Implemented Name and Department information extraction from CV
- Implemented Name validaiton from our lookup table collected from webscrapping

## Backend

### Goals

- The database will house all of the information scrapped from the various CVs to be used when searching for research opportunities

### Methods, Practices, and Tools

- For the database we will be using MySQL
- We will be using Python along with the Django Framework to access the MySQL database and manipulate the stored data
- For development purposes the database will be hosted on our local machines but in the future we plan on using an online database to allow for development using the same database.

### Current Progress
- We have a simple database designed, we can add different data as we need it
- Can connect to the database with an online server using Django
- Automatically read csv files and add data to the Django database, while avoiding duplicate values
- We are now able to connect to the database and display data on the results webpage
- We are able to enter a search value on the webpage and return data from the db according to the search query
- Returned interests from that same faculty member will now be listed under one name instead of one name for each interest
- May now upload CVs from the website that are automatically scrapped and added to the database.
- Radial button on the website now returns the correct data from the database depending on the selected option and search query.
- Now when uploading a CV it is scrapped and the data is displayed on the webpage to be checked by the user before being added to the database.
- Inserted text now gets inserted to the database correctly
- Added more tables to support more faculty information
