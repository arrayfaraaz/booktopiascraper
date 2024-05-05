#importing relevant packages
from bs4 import BeautifulSoup
import requests
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

#defining the function to get desired information from the website
def book_data(isbn):
    response = requests.get(f"https://www.booktopia.com.au//book/{isbn}.html", headers=headers).text
    soup = BeautifulSoup(response, 'html.parser')
    title = soup.find('h1', {"class":"MuiTypography-root MuiTypography-h1 mui-style-1ngtbwk"})
    author = soup.find('span', {"id":"MuiTypography-root MuiTypography-body1 mui-style-1plnxgp"})

    if title and author:
        title.text.strip()
        author.text.strip()
        return title, author
    else:
        return "Book data Not Found", "Book data Not Found"

# fetching each isbn number from the input_list.csv file and storing it into a list
isbn_list = []
with open('input_list.csv', 'r', newline='') as file: # reading the input csv file
    reader = csv.reader(file)
    for line in reader:
        isbn = line[0].strip()  # Accessing the first element of the row (ISBN)
        if isbn:
            isbn_list.append(isbn)

#storing the title and author data into another list
book_list = []
for isbn in isbn_list:
    title, author,  = book_data(isbn=isbn) # calling the function 
    book_list.append({'ISBN': isbn, 'Title': title, 'Author': author})


#writing the scraped info from the website to another csv file
with open('output_data.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['ISBN', 'Title', 'Author'])
    writer.writeheader()
    for book in book_list:
         writer.writerow(book)

    








