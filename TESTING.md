# Testing Documentation
## Frontend
- Tested Figma prototype to implement overlays. Failed at first, and then implemented them using hovering and manual positioning.
- Have been having trouble testing how to format the links for finding funding. Decided to follow the [funding page](https://www.bgsu.edu/research-economic-development/office-of-sponsored-programs-and-research/funding.html) on bgsu's site.
- When building the html/css templates have been having trouble centering/aligning the BGSU logo and "Faculty Collaboration" in the header. first tried "vertical-align" but had to use padding instead.
- In our first demo we had good responses on the look and lay out of the UI which was good to hear.
- Had to trouble shoot how to change the font-size units from pixels to rem. Had to set base font-size to 20px first.
- Tested implementing update button in nav bar. All went good first try.
- Have been trying to center buttons on update page. Margin auto and text-align didn't work. Ended up wrapping them in divs.
- Wasn't able to use range in for loop to iterate from second element. Ended up using an if statement to skip first element on results page for research interests.
- We tested the wording of our paragraphs with a review from the customer and gave changes to be made.
- Have been having issues with my CSS files being compiled. For some reason the interpretter does not use the most up to date ones which has made it harder to develop and format. Still unsure why besides the mounted directory being slow to update.
- Still having issues with the CSS. I believe its just going to be an ongoing problem since we are working remotely. Since I get this warning everytime I open the project "External file changes sync may be slow: Project files cannot be watched (are they under network mount?)". Will continue to look for a solution though.
- Tested that all active webpages now link to the homepage through the BGSU logo.
- Have been trouble shooting ways to get around the css issue and have begun by trying to edit code viw winscp and compiling in a putty terminal with a tunnel to my local machine.
- Tested that text inserted into the text boxes will get inserted to the database
- Winscp with a putty terminal allows css to work correctly. Will not be using pycharm for much in the future anymore.
- Tested that the upload page will populate the fields with current database information if you are logged in and have data in the database.
- Right now all the collapsibles start open and I have been trouble shooting and am not sure why still testing.
- Tested styling the collapsibles inline and then put into seperate css file.

## Backend
- Tested multiple CV's for text mining to extract research interests
    - Still need to generalize the approach some more and allow users to validate the data
- Tested more ways to generalize research interest scrapping to include common delimiters
- Tested code to scrap the department from a CV
- When moved to Linux VM had issues with hardcoded file paths. THe solution we found to work best has getting the current working directory via Python's OS module and prepending to the relative file paths. This way it works on everyones machines.
- Tested that scrapping code correctly scraps the data from an uploaded CV and insert that to the database
- Implemented and Tested the new radial menu to make sure that it returns the correct results based on the selected option.
- Text scrapped from CV's gets inserted into the text boxes on the upload page 

## Database
- Tested the SQL database to upload/input new data using Django.
- Tested inputing duplicate data into the database. We were able to prevent duplicate data from being inserted successfully.
- Searching the database with a search bar has been tested and works as expected. We search on substring matching.
- Tested that searching a research intrest will show a faculty member exactly once and all of their research interest.
- Tested that previous user data gets removed and replaced when a CV gets uploaded. This updates the users information
- Tested different search values and realized certain input would return incorrect data. Bug was squashed.

## Webscrapping
- Tested that we can webscrape names, emails, department, and phone numbers from BGSU's staff directory page
- Tested that this data is consistent and can be used to get more information from a persons name, in lieu of SSO
