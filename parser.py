import requests
from bs4 import BeautifulSoup
import time
import re


ID = 'ID'
PW = 'PW'


w_boards = [
    "http://www.renjukorea.com/bbs/board.php?board=kkkgibow1989",
    "http://www.renjukorea.com/bbs/board.php?board=kkkgibow2001",
    "http://www.renjukorea.com/bbs/board.php?board=kkkgibow2003",
    "http://www.renjukorea.com/bbs/board.php?board=kkkgibow2005",
    "http://www.renjukorea.com/bbs/board.php?board=kkkgibow2007",
    "http://www.renjukorea.com/bbs/board.php?board=kkkgibow2009",
    "http://www.renjukorea.com/bbs/board.php?board=kkkgibow2011",
    "http://www.renjukorea.com/bbs/board.php?board=kkkgibow2013",
    "http://www.renjukorea.com/bbs/board.php?board=kkkgibow2015",
]
wt_boards = [
    "http://www.renjukorea.com/bbs/board.php?board=kkkgibowt2002",
    "http://www.renjukorea.com/bbs/board.php?board=kkkgibowt2004",
    "http://www.renjukorea.com/bbs/board.php?board=kkkgibowt2006",
    "http://www.renjukorea.com/bbs/board.php?board=kkkgibowt2008",
    "http://www.renjukorea.com/bbs/board.php?board=kkkgibowt2010",
    "http://www.renjukorea.com/bbs/board.php?board=kkkgibowt2012",
]
asia_boards = [
    "http://www.renjukorea.com/bbs/board.php?board=kkkgiboasia",
    "http://www.renjukorea.com/bbs/board.php?board=kkkgiboasia2"
]
uro_boards = [
    "http://www.renjukorea.com/bbs/board.php?board=kkkgibouro1996",
    "http://www.renjukorea.com/bbs/board.php?board=kkkgibouro2006",
    "http://www.renjukorea.com/bbs/board.php?board=kkkgibouro2008",
]
ko_boards = [
    ("http://www.renjukorea.com/bbs/board.php?board=kkkgibokotop", range(3, 10), []),
    ("http://www.renjukorea.com/bbs/board.php?board=kkkgibokorank", range(13, 21), ['']),
    ("http://www.renjukorea.com/bbs/board.php?board=kkkgibokomaster", range(1, 4), []),
]
ja_boards = [
    ("http://www.renjukorea.com/bbs/board.php?board=kkkgibojatops", range(38, 52), []),
]
etc_boards = [
    "http://www.renjukorea.com/bbs/board.php?board=kkkgibstockholm",
    "http://www.renjukorea.com/bbs/board.php?board=kkkgibswecham07",
    "http://www.renjukorea.com/bbs/board.php?board=kkkgib4thfishparty",
]


### will be added more links above...

all_boards = [
    w_boards,
    wt_boards,
    asia_boards,
    uro_boards,
    ko_boards,
    ja_boards,
    etc_boards
]


def login(id, pw):
    r = requests.post("http://www.renjukorea.com/bbs/member.php",
                      data={
                          'mboard': 'memberboard',
                          'exe': 'login_act',
                          'login_after_url': 'board.php?board=kkkmain&command=skin_insert&exe=insert_iboard1_home',
                          'target': '',
                          'm_id': id,
                          'm_pass': pw,
                          'x': '17',
                          'y': '27'
                      })
    return r.cookies


def parse(url, cookies):
    r = requests.get(url, cookies = cookies)
    text = r.content.decode('euc-kr')
    soup = BeautifulSoup(text, 'html.parser')
    gibo = soup.find('applet').find('param', attrs={"name": "moves"}).get('value')

    t = soup.find('div', {'id' : 'mainTextBodyDiv'})

    white_flag = "백승" in str(t)
    black_flag = "흑승" in str(t)
    draw_flag = "무승부" in str(t)

    if white_flag and not black_flag and not draw_flag:
        winner = 'white'
    elif not white_flag and black_flag and not draw_flag:
        winner = 'black'
    elif not white_flag and not black_flag and draw_flag:
        winner = 'draw'
    else:
        print(t)
        winner = 'unknown'

    return winner, gibo


def parse_board(board, start_no, f):
    common_link = board + "&command=body&no="
    no = start_no
    while True:
        link = common_link + str(no)
        print("------------------------------")
        try:
            winner, gibo = parse(link, cookies)
            print("Url :", link)
            print("Winner :", winner)
            print("Gibo :", gibo)
            f.write("{0} {1} {2}\n".format(link, winner, gibo))
            no += 1
            global cnt
            cnt += 1
        except Exception as e:
            print("Exception occurs when parsing", link)
            print(e)
            time.sleep(0.2)
            if no > 4:
                break
            else:
                no += 1
        finally:
            print("------------------------------")
            time.sleep(0.1)


cnt = 0
f = open('data.txt', 'w')
cookies = login(ID, PW)
for g_boards in all_boards:
    print("> parse g_boards")

    if g_boards == ko_boards or g_boards == ja_boards:
        boards = []
        for common_board, no_list, postfix_exs in g_boards:
            for no in no_list:
                boards.append((common_board + str(no), 1))
            for postfix in postfix_exs:
                boards.append((common_board + str(postfix), 26))
    else:
        boards = g_boards

    for board in boards:

        if g_boards == asia_boards:
            start_no = 2
            board_url = board
        elif g_boards == ko_boards or g_boards == ja_boards:
            board_url, start_no = board
        else:
            start_no = 1
            board_url = board

        print(">> parse board :", board_url)

        parse_board(board_url, start_no, f)

print("All # of Gibo :", cnt)
f.close()
