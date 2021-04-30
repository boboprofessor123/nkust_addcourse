from bs4 import BeautifulSoup
import requests
import re
import threading
import time
import urllib3

urllib3.disable_warnings()
def create_session():
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        }
    client = requests.session()
    client.headers.update(headers)
    client.verify = False
    return client

def get_token(client):

    token_res = client.get('https://aais7.nkust.edu.tw/selcrs_std').text
    token_soup = BeautifulSoup(token_res,'html.parser')
    token = token_soup.find_all('input',type='hidden')[1]['value']
    return token

def login(client,token):
    login_info = {
        '__RequestVerificationToken': token,
        'Url': '',
        'UserAccount': 'C107110143',
        'Password': 'bobo123'
    }

    login_res = client.post('https://aais7.nkust.edu.tw/selcrs_std/Login',data=login_info)


def get_class(info):
    while True:
        client = create_session()
        token = get_token(client)
        login(client,token)
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            }
        first_post = client.get('https://aais7.nkust.edu.tw/selcrs_std/AddSelect/AddSelectPage')
        tokenss_soup = BeautifulSoup(first_post.text,'html.parser')
        tokenss = tokenss_soup.find_all('input',type='hidden')[-1]['value']

        cookies = first_post.cookies

        client.headers.update(
                {
                    'RequestVerificationToken': tokenss,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            )
        for i in info:
            time.sleep(1)
            add_post = client.post('https://aais7.nkust.edu.tw/selcrs_std/AddSelect/AddSelectCrs',data=i,cookies=cookies,headers=headers).text
            if i == add_info2:
                print('歷史' + add_post)
            elif i == add_info3:
                print('核一' + add_post)
            elif i == add_info4:
                print('服務創新(七,八)' + add_post)
            elif i == add_info5:
                print('在地文化(七,八)' + add_post)


add_info2 = {  #歷史
    'CrsNo': '4381',
    'PCrsNo': '042C01582',
    'SelType': 'O',
}
add_info3 = {  #核一
    'CrsNo': '4204',
    'PCrsNo': '042C00665',
    'SelType': 'O',
}
add_info4 = {  #服務創新(七,八)
    'CrsNo': '4452',
    'PCrsNo': '042C00882',
    'SelType': 'O',
}
add_info5 = {  #在地文化(七,八)
    'CrsNo': '4200',
    'PCrsNo': '042C00607',
    'SelType': 'M',
}
add_info6 = {  #多媒體(一,二)
    'CrsNo': '4472',
    'PCrsNo': '042C00895',
    'SelType': 'M',
}

get_class([add_info2,add_info3,add_info4,add_info5])