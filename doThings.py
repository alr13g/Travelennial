from bs4 import BeautifulSoup
import json
import requests
import re
import time
import io

def getAttractions(locality):

    url = ""

    geocodes = [['Tallahassee', 'https://www.tripadvisor.com/Attractions-g34675-Activities-Tallahassee_Florida.html'],

                ['Boston', 'https://www.tripadvisor.com/Attractions-g60745-Activities-Boston_Massachusetts.html'],

                ['Atlanta', 'https://www.tripadvisor.com/Attractions-g60898-Activities-Atlanta_Georgia.html'],

                ['Chicago', 'https://www.tripadvisor.com/Attractions-g35805-Activities-Chicago_Illinois.html'],

                ['Los Angeles', 'https://www.tripadvisor.com/Attractions-g32655-Activities-Los_Angeles_California.html'],

                ['Dallas', 'https://www.tripadvisor.com/Attractions-g55711-Activities-Dallas_Texas.html'],

                ['Denver', 'https://www.tripadvisor.com/Attractions-g33388-Activities-Denver_Colorado.html'],

                ['New York', 'https://www.tripadvisor.com/Attractions-g60763-Activities-New_York_City_New_York.html'],

                ['San Francisco', 'https://www.tripadvisor.com/Attractions-g60713-Activities-San_Francisco_California.html']]


    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
    headers = { 'User-Agent' : user_agent }

    ta_url = 'http://www.tripadvisor.ca'
    base_url = ""
    location_url = ""

    #get base and location url's
    for code in geocodes:
        if code[0] == locality:
            location_url = str(code[1])[58:]
            counter = 0;
            for c in reversed(str(code[1])):
                counter = counter + 1
                if c == "-":
                    index = counter - 1
                    base_url = str(code[1])[:- index]


    activities = []

    dl_page_src(base_url + location_url)

    with open('tripadvisor.html', encoding='utf-8') as page_src:
        source = page_src.read()

    soup = BeautifulSoup(source, 'html.parser')
    
    # get the lazy loaded image list
    image_list = get_image_list(soup)
    
    # get last element in the pagenation (i.e.: total number of pages)
    page_count = int(soup.select('.pagination a')[-1].text.strip())
    for page_no in range(page_count):
        # our formula to compute the next url to download:
        # [page_no * 30]
        # page 1: base_url + location_url
        # page 2: base_url + 'oa' + [page_no * 30] + '-' + location_url
        # etc ...
        page_results = soup.select('#FILTERED_LIST .attraction_element')

        # loop over all elements and extract the useful data
        for result in page_results:
            title = result.select('.property_title a')[0].text.strip()
            
            rating_obj = result.select('.rate_no')
            pattern = re.compile('\srate_no\sno(\d{2})"')
            matches = pattern.search(str(rating_obj))
            if matches:
                print(matches.group(1))
                rating = matches.group(1)
                total_reviews = result.select('.rating .more a')[0].text.strip().replace(' reviews', '')
            else:
                rating = '0'
                total_reviews = '0'
            
            popularity = result.select('.popRanking')[0].text.strip()
            review_url = ta_url + result.select('a.photo_link')[0]['href']
            
            # get image url
            lazy_load_obj = result.select('.photo_booking a img')
            if lazy_load_obj[0].has_attr('id'):
                lazy_load_id = lazy_load_obj[0]['id']
                image_obj = [x['data'] for x in image_list if x['id'] == lazy_load_id]
                image_url = image_obj[0]
            else:
                image_url = 'static/images/generic.jpg'
            
            activities.append({
                'title': title,
                'rating': rating,
                'reviews': total_reviews,
                'popularity': popularity,
                'review_url': review_url,
                'image_url': image_url
            })

        # compute the url for the next page
        next_page = base_url + 'oa' + str((page_no + 1) * 30) + '-' + location_url

        time.sleep(15)
        dl_page_src(next_page)
        
        with io.open('tripadvisor.html', encoding='utf-8') as page_src:
            source = page_src.read()
            
        soup = BeautifulSoup(source, 'html.parser')
        
        # get the lazy loaded image list
        image_list = get_image_list(soup)

    #with io.open('activities.json', 'w') as output:
    #    output.write(json.dumps(activities, indent=4))

    return activities

def dl_page_src(url):
    print(url)
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
    headers = { 'User-Agent' : user_agent }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    with io.open('tripadvisor.html', 'w') as saved_page:
        saved_page.write(soup.prettify().decode('utf-8').encode('utf-8'))
        
def get_image_list(soup):
    # get all the script tags then get the one that contains the line
    # 'var lazyImgs'
    script_tags = soup.find_all('script')
    pattern = re.compile('var\s*?lazyImgs\s*?=\s*?(\[.*?\]);', re.DOTALL)
    
    for tag in script_tags:
        matches = pattern.search(tag.text)    
        if matches:
            image_list = json.loads(matches.group(1))
            return image_list