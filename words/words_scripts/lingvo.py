import requests, os


def auth():
    lingvo_key = os.environ.get('LINGVO_KEY')
    h = {'Authorization': f'Basic {lingvo_key}'}
    url = 'https://developers.lingvolive.com/api/v1.1/authenticate'
    get_key = s.post(url=url, headers=h)
    return get_key.text


def get_json(h, p, api):
    url = f'https://developers.lingvolive.com/api/v1/{api}'
    return s.get(url=url, params=p, headers=h).json()


def get_data(word):
    global headers, s, search
    search = word
    with requests.Session() as s:
        key = auth()
        headers = {'Authorization': f'Bearer {key}'}
        # word = re.sub(r'[\'\"]', '', word)
        minicard = get_json(headers, dict(text=word, srcLang=1033, dstLang=1049), 'Minicard')
        collocation = get_json(headers, dict(prefix=word, srcLang=1033, dstLang=1049, pageSize=20), 'WordList')
        wordform = get_json(headers, dict(text=word, lang=1033), 'WordForms')
    return minicard, collocation, wordform


def get_word_form(js_data):
    words = []
    for row in js_data:
        if row['ParadigmJson']['Groups']:
            words.append([row['ParadigmJson']["Grammar"]])
            for group in row['ParadigmJson']['Groups']:
                words.append([group['Name']])
                for v in group['Table']:
                    for w in v:
                        words[-1].append((w["Prefix"] or '').capitalize() + w['Value'])
    return words


def parse_json(js_data):
    tree = js_data[0]
    sound = tree["Translation"]["SoundName"]
    params = dict(dictionaryName='LingvoUniversal (En-Ru)', fileName=sound)
    sound_file = s.get(url='https://developers.lingvolive.com/api/v1/Sound', params=params, headers=headers)
    phrases = [(word["Heading"], word["Translation"]) for word in js_data[1]["Headings"]]
    forms_words = get_word_form(js_data[2])
    link = requests.get('https://dictionary.skyeng.ru/api/public/v1/words/search',
                        params={'search': search}).json()[0]["meanings"][0]["imageUrl"]
    word_img = link[link.find('https:'):]

    return {
        'sound': sound,
        'sound_file': sound_file.json(),
        'phrases': phrases,
        'forms_words': forms_words,
        'word_img': word_img,
    }
