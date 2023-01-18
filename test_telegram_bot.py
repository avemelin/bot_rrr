from bs4 import BeautifulSoup
from telegraph.api import Telegraph
import requests
import telebot


def add_src(code):
    while code.find('src="/uplo') > -1:
        x = code.find('src="/') + 5
        code = code[:x] + 'https://www.menslife.com' + code[x:]
    return code


def del_tag(code, tag):
    while code.find(tag) > -1:
        x = code.find(tag)
        code = code[:x] + '<br><br>' + code[x + len(tag):]
    return code


def make_telegraph(token, title, photo, photo_text, main_text):
    session = Telegraph(token)

    tag = del_tag(del_tag('\n'.join(str(main_text).split('\n')[1:]), '<h2>'),
                  '</h2>')
    tag = str(photo) + '\n' + tag
    tag = del_tag(tag, '/div')
    tag = add_src(tag)
    return session.create_page(title=title, author_name='@muzhik_zdorov',
                               html_content=tag.strip()[:-5].rstrip('<').rstrip(
                                   '<<br>'))


bot = telebot.TeleBot('1112028335:AAFRZ_eALJvPsNtzjdTLsbdnBHwbUh1gxn8')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, кинь мне ссылку')


@bot.message_handler(content_types=['text'])
def send_text(message):
    url = message.text
    token = 'e05180aaf37d7293ad9bfc1e3df510b7b6adc642e685da38f8068a222d8d'
    soup = BeautifulSoup(
        requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text,
        'html.parser')
    title = soup.find_all('h1')[0].text
    desc_tlg = soup.find('div', class_='detail-anons').text
    photo = soup.find_all('img')[8]
    photo_text = soup.find_all('img')[8]['alt']
    main_text = soup.find('div', class_='detail-text')
    # print(str(soup.find('div', class_='detail-text')).split('\n'))
    href = make_telegraph(token, title, photo, photo_text, main_text)
    bot.send_message(message.chat.id,
                     "<strong>" + title + "</strong>\n\n" + desc_tlg.strip() + "\n\n" + str(
                         href['url']),
                     parse_mode='HTML')



if __name__ == '__main__':
    bot.polling()
