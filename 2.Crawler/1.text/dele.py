from bs4 import BeautifulSoup as BS
import urllib.request


OUTPUT_FILE_NAME = 'output.txt'

URL = 'http://www.lotteimall.com/display/sellRank100GoodsList.lotte'


def get_text(URL):
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BS(source_code_from_URL, 'html.parser', from_encoding='utf-8')
    text = ''
    for item in soup.find_all('li'):
        text = text + str(item.find_all(text=True))
    return text


def main():
    open_output_file = open(OUTPUT_FILE_NAME, 'w')
    result_text = get_text(URL)
    open_output_file.write(result_text)
    open_output_file.close()


if __name__ == '__main__':
    main()

