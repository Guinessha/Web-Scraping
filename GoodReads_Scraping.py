from bs4 import BeautifulSoup
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

books = []
# Set up retry strategy
retry_strategy = Retry(
    total=3,  # Total retries
    backoff_factor=1,  # Delay between retries
    status_forcelist=[429, 500, 502, 503, 504],  # Status codes to retry
    allowed_methods=["HEAD", "GET", "OPTIONS"]  # Allowed methods to retry
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

for i in range(1,100):
    url = 'https://www.goodreads.com/list/show/1.Best_Books_Ever?page={i}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }


    try:
        response = http.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        response_content = response.text
        #print(response_content)

        # Parsing the HTML content
        soup = BeautifulSoup(response_content, 'html.parser')

        # Example to extract book titles from the page
        articles = soup.find_all('tr', {'itemscope': ''})
        for article in articles:
            book_title = article.find('a', class_='bookTitle').text.strip()
            author_book = article.find('a', class_='authorName').text.strip()
            star_book = article.find('span', class_='minirating').text
            star_book = star_book[1:5]
            review = article.find('span', class_='minirating').text
            review = review[19:28]
            book_url = "https://www.goodreads.com" + article.find('a', {'class': 'bookTitle'})['href']
            books.append([book_title, author_book, star_book, review, book_url])
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

df = pd.DataFrame(books, columns=['Title', 'Author', 'Star Ranting', 'Sum Review', 'URL'])

df.to_csv('books.csv', index=False)