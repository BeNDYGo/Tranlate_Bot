import requests
import bs4
import asyncio
from googletrans import Translator

translator = Translator()

def get_translate_wooo(word):
    def fetch_page(word):
        url = f'https://wooordhunt.ru/word/{word}'
        response = requests.get(url)
        return bs4.BeautifulSoup(response.text, 'lxml')
    def translate(soup):
        content = soup.find(class_='t_inline_en')
        if content: return content.text
        block = soup.find(class_='t_inline')
        if block: return block.text
        return None
    if ' ' in word: return None
    word_page = fetch_page(word)
    return translate(word_page)

async def get_translate_google(wood):
    resultEN = await translator.translate(wood, dest="en")
    resultRU = await translator.translate(wood, dest="ru")
    print(resultEN, resultRU)
    for translare in (resultEN.text, resultRU.text):
        if translare.lower() != wood.lower(): 
            return translare


async def get_translate(word):
    wooo_translate = get_translate_wooo(word)
    google_translate = await get_translate_google(word)
    return wooo_translate, google_translate


async def main():
    while True:
        word = input('Слово: ')
        res = await get_translate(word)
        print(res)
if __name__ == '__main__':
    asyncio.run(main())
