# Waw-Cinema-Assistant

This Python project aims to create a personal assistant for movie enthusiasts in Warsaw. 
Using web scraping with Beautiful Soup 4 and Flask, 
it extracts relevant information from the websites of two popular cinemas in Warsaw: Amondo and Iluzjon. 

**The entire project is deployed on Google Cloud Run, ensuring scalability and automated resource management.**

## Features
* **Movie Data Scraping:** Retrieves movie titles, showtimes, and link to a movie discription.
* **Data Extraction:** Utilizes Beautiful Soup 4 for efficient HTML parsing and data extraction.
* **Multithreading:** Speeds up data retrieval from multiple pages simultaneously using multithreading.
* **Integration with IMDb:** Leverages the IMDb library to fetch additional movie information such as ratings.
* **Python-Based:** Built using Python, a versatile and popular programming language for data science and automation.
* **Deployed on Google Cloud Run:** The application is deployed on the serverless Google Cloud Run platform,
                                                                  ensuring automated scaling and resource management.

## Technologies Used
* **Beautiful Soup 4:** A Python library for parsing HTML and XML documents.
* **IMDbPY:** A Python library for interacting with the IMDb movie database.
* **Flask:**  A lightweight and flexible Python web framework.
* **Google Cloud Run:** A serverless platform for running the application.

## Project Structure
* **main.py:** The main script coordinating the scraping process.
* **templates:** Directory containing HTML templates for the web interface.
* **static:** Directory for storing static files like CSS and JavaScript.
* **requirements.txt:** A file listing project dependencies.
* **Amondo.py:** A class for scraping Amondo's website.
* **Iluzjon.py** A class for scraping Iluzjon's websit.
* **Movie.py:** A class for fetching movie information.

## Future Improvements
* **User Interface:** Developing a more intuitive user interface, e.g., using a web framework.
