import requests
import pprint

user = 'rpifer@udel.edu'
pwd = 'UtHGRSFfmlSXVvxIvDX'

url_login = 'http://en.boardgamearena.com/account/account/login.html'
prm_login = {'email': user, 'password': pwd, 'rememberme': 'on',
             'redirect': 'join', 'form_id': 'loginform'}
tableID = '97327775'
url_game = 'http://en.boardgamearena.com/1/connectfour?table=' + tableID
url_log = 'http://en.boardgamearena.com/archive/archive/logs.html'
prm_log = {'table': tableID, 'translated': 'true'}

with requests.session() as c:
    r = c.post(url_login, params=prm_login)
    if r.status_code != 200:
        print(r.status_code)
        print('Error trying to login')

    r = c.get(url_game)
    if r.status_code != 200:
        print('Error trying to load the gamereview page')

    # print(r.text)
    r = c.get(url_log, params=prm_log)
    if r.status_code != 200:
        print('Error trying to load logs')

    log = r.text

    r = c.get('https://boardgamearena.com/1/connectfour/connectfour/playDisc.html?x=1&table=97327775')

    print(r.text)


