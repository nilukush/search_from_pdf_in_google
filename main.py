import PyPDF2
import requests
from bs4 import BeautifulSoup
import json


def search_google(name):
    url = f"https://www.google.com/search?q={name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    return response.text


def extract_data_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    # Extract the desired data from the HTML using BeautifulSoup selectors
    # You can customize this part based on the specific information you want to extract
    # For example, you can extract the title, snippet, or URL of each search result
    search_results = soup.select('.tF2Cxc')
    data = []
    for result in search_results:
        title = result.select_one('.DKV0Md').text
        snippet = result.select_one('.VwiC3b').text
        url = result.a.get('href')
        data.append({
            'title': title,
            'snippet': snippet,
            'url': url
        })
    return data


def main():
    # Open the PDF file
    with open('names.pdf', 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        names = [page.extract_text().strip() for page in reader.pages]

    # Iterate through the names and search in Google
    search_results = []
    for name in names:
        html = search_google(name)
        results = extract_data_from_html(html)
        search_results.append({
            'name': name,
            'results': results
        })

    # Save the search results to a file (you can choose the desired format, e.g., JSON, CSV)
    with open('search_results.json', 'w') as file:
        json.dump(search_results, file)


if __name__ == "__main__":
    main()
