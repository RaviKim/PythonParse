
import requests
from bs4 import BeautifulSoup as BS
 
def mnet_Crawling(html):
    temp_list = []
 
    tr_list = html.select('div.MnetMusicList.MnetMusicListChart > div.MMLTable.jQMMLTable > table > tbody > tr')
 
    for tr in tr_list :
        rank = int(tr.find('td',{'class':'MMLItemRank'}).find('span').text.strip('위'))
 
        img = tr.find('td',{'class':'MMLItemTitle'}).find('div',{'class':'MMLITitle_Album'}).find('img')['src']
        img = tr.find('td',{'class':'MMLItemTitle'}).find('div',{'class':'MMLITitle_Album'}).find('img').get('src')
 
        title = tr.find('td',{'class':'MMLItemTitle'}).find('div',{'class':'MMLITitle_Box info'}).find('a',{'class':'MMLI_Song'}).text
        artist = tr.find('td',{'class':'MMLItemTitle'}).find('div',{'class':'MMLITitle_Box info'}).find('a',{'class':'MMLIInfo_Artist'}).text
        album = tr.find('td',{'class':'MMLItemTitle'}).find('div',{'class':'MMLITitle_Box info'}).find('a',{'class':'MMLIInfo_Album'}).text
        temp_list.append([rank, img, title, artist, album])
 
 
 
    return temp_list
#============================================================ End of mnet_Crawling() ============================================================#
 
mnet_list = []
 
req = requests.get('http://www.mnet.com/chart/TOP100/')
 
for page in [1,2]:
    req = requests.get('http://www.mnet.com/chart/TOP100/?pNum={}'.format(page))
    html = BS(req.text, 'html.parser')
    
    mnet_list += mnet_Crawling(html)
 
 
# 리스트 출력
for item in mnet_list :
    print(item)
 




