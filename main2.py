import requests
from bs4 import BeautifulSoup

dataFileName = 'dataFile.txt'

def read_google_doc_public(doc_url):
    # Ensures the URL is the published version ending in '/pub'
    if not doc_url.endswith('/pub'):
        print("Please use the 'publish to web' URL for this method.")

    response = requests.get(doc_url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract all text from the body
        text = soup.get_text(separator='\n')
        with open(dataFileName, 'w', encoding='utf-8') as file:
            file.write(text)
    else:
        print(f"Access error: {response.status_code}")

    with open(dataFileName, 'r') as file:
        for line in file:
            if 'y-coordinate' in line:
                break
        lines = file.readlines()
        
    coordinates = []    #List of tuples, index 0 is x-coordinate, index 1 is character, index 2 is y coordinate
    maxXCoord = 0
    maxYCoord = 0
    for i in range(1, len(lines), 3):    #Appends data to tuples and finds maximum coords for mapping data, skipping first 4 lines
        xCoord = int(lines[i-1].strip())
        yCoord = int(lines[i + 1].strip())
        coordinates.append((xCoord, lines[i].strip(), yCoord))
        if xCoord > maxXCoord:
            maxXCoord = xCoord

        if yCoord > maxYCoord:
            maxYCoord = yCoord

    charMap = [[' ' for i in range(maxXCoord + 1)] for i in range(maxYCoord + 1)] #Map for all the spots characters could go

    for i in coordinates:
        charMap[i[2]][i[0]] = i[1]  #Assigns characters to certain places on the mao

    charMap.reverse()
    for i in charMap:
        print(*i, sep='')

# Example usage:
doc_url = 'https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub'
read_google_doc_public(doc_url)
