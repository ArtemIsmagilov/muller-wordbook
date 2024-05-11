import sys
import xml.etree.ElementTree as ET
import sqlite3
import threading
import queue


def get_line(ar):
    tr = ar.find('tr')
    eng = ar.find('k')
    if tr is not None:
        transcription = "| %s |" % tr.text
        rus = tr.tail
        return eng.text.strip(), transcription.strip(), rus.strip()
    else:
        rus = eng.tail
        return eng.text.strip(), None, rus.strip()


def insert_word(element):
    cur.execute("INSERT INTO words_word(eng, tr, rus) VALUES(?, ?, ?);", get_line(element))


def run_sqlite3():
    con = sqlite3.connect('db.sqlite3', check_same_thread=False)
    inserting(con)


def worker():
    while True:
        e = q.get()
        insert_word(e)
        q.task_done()


def inserting(con):
    global q, cur
    cur = con.cursor()

    tree = ET.parse('words/words_scripts/dict.xdxf')
    root = tree.getroot()
    q = queue.Queue()
    threading.Thread(target=worker, daemon=True).start()

    for element in root.findall('ar'):
        q.put(element)

    q.join()
    con.commit()
    cur.close()
    con.close()

    print('All work completed')


def run():
    run_sqlite3()


if len(sys.argv) == 2 and sys.argv[1] == 'run':
    run()
