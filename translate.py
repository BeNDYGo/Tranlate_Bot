import requests
import bs4


def get_translate(word):
    def fetch_page(word):
        url = f'https://wooordhunt.ru/word/{word}'
        response = requests.get(url)
        return bs4.BeautifulSoup(response.text, 'lxml')
    def translate(soup):
        content = soup.find(class_='t_inline_en')
        if content: return content.text
        block = soup.find(class_='t_inline')
        if block: return block.text
        return 'ошибка'


    word_page = fetch_page(word)
    return translate(word_page)

if __name__ == '__main__':
    while True:
        word = input('Слово: ')
        #word = 'fetch'
        print(get_translate(word))
