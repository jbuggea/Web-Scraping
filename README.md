# Web-Scraping

This code employs several different methods. First I use BeautifulSoup to scrape the website finds.org.uk for the latest 
100 artefacts uploaded on its site. I first get the first 100 links from the search engine, then open each link in turn. 
As each link is opened I scrape the object name, description, record ID and image. The former two are placed into an SQLite 
Database. The image is opened and written into a dedicated directory, under the Record ID name. This name will then correspond 
to the Record ID (image reference) in the database, so it can be placed correctly on the webpage. Finally I use Flask to 
create a webpage showing the first ten objects. This calls all rows in the database with a limit of ten rows. So, in 
conjunction with a html template that is referenced in the file, the data is passed through to be displayed on the webpage.  
The html uses paragraph breaks and table indentations to aid clarity of viewing. 
