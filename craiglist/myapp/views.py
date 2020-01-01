import requests
from django.shortcuts import render
from requests.compat import quote_plus
from bs4 import BeautifulSoup

# Create your views here.

BASE_URL_CRAIGLIST_BANGALORE = 'https://bangalore.craigslist.org/search/sss?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'
def search(request):
    return render(request, 'myapp/base.html')

def new_search(request):
    searched = request.POST.get('search')
    # print(searched)
    final_url = BASE_URL_CRAIGLIST_BANGALORE.format(quote_plus(searched))
    response = requests.get(final_url)
    data = response.text

    print('Waseem : response ends')

    soup = BeautifulSoup(data, features='html.parser')
    post_listing = soup.find_all('li', {'class':'result-row'})
	
    final_posting = []
	
    for post in post_listing:
        post_title = post.find(class_="result-title").text
        post_url = post.find('a').get('href')
		
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'NA'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids')
            print('post_image-id: ', post_image_id)
            post_image_id = post_image_id.split(':')[1]
            post_image_id = post_image_id.replace(',1','')
            #print('image id :', post_image_id)
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_posting.append((post_title, post_url, post_price, post_image_url))
		
    context = {

    'searched' : searched,
    'final_posting' : final_posting,

    }
			
    # f = open(r'C:\Users\Waseen\Desktop\wesponse.txt','w', encoding="utf-8")
    # f.write(str(post_listing))
    # f.close()
    return render(request, 'myapp/new_search.html', context)
