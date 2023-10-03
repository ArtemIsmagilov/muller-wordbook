from django import forms

from captcha.fields import CaptchaField

LANGS = ('af', 'Afrikaans'), ('sq', 'Albanian'), ('am', 'Amharic'), ('ar', 'Arabic'), ('hy', 'Armenian'), ('as', 'Assamese*'), ('ay', 'Aymara*'), ('az', 'Azerbaijani'), ('bm', 'Bambara*'), ('eu', 'Basque'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('bho', 'Bhojpuri*'), ('bs', 'Bosnian'), ('bg', 'Bulgarian'), ('ca', 'Catalan'), ('ceb', 'Cebuano'), ('(Simplified)', 'Chinese'), ('(Traditional)', 'Chinese'), ('co', 'Corsican'), ('hr', 'Croatian'), ('cs', 'Czech'), ('da', 'Danish'), ('dv', 'Dhivehi*'), ('doi', 'Dogri*'), ('nl', 'Dutch'), ('en', 'English'), ('eo', 'Esperanto'), ('et', 'Estonian'), ('ee', 'Ewe*'), ('(Tagalog)', 'Filipino'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('gl', 'Galician'), ('ka', 'Georgian'), ('de', 'German'), ('el', 'Greek'), ('gn', 'Guarani*'), ('gu', 'Gujarati'), ('Creole', 'Haitian'), ('ha', 'Hausa'), ('haw', 'Hawaiian'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hmn', 'Hmong'), ('hu', 'Hungarian'), ('is', 'Icelandic'), ('ig', 'Igbo'), ('ilo', 'Ilocano*'), ('id', 'Indonesian'), ('ga', 'Irish'), ('it', 'Italian'), ('ja', 'Japanese'), ('jv', 'Javanese'), ('kn', 'Kannada'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('rw', 'Kinyarwanda'), ('gom', 'Konkani*'), ('ko', 'Korean'), ('kri', 'Krio*'), ('ku', 'Kurdish'), ('(Sorani)*', 'Kurdish'), ('ky', 'Kyrgyz'), ('lo', 'Lao'), ('la', 'Latin'), ('lv', 'Latvian'), ('ln', 'Lingala*'), ('lt', 'Lithuanian'), ('lg', 'Luganda*'), ('lb', 'Luxembourgish'), ('mk', 'Macedonian'), ('mai', 'Maithili*'), ('mg', 'Malagasy'), ('ms', 'Malay'), ('ml', 'Malayalam'), ('mt', 'Maltese'), ('mi', 'Maori'), ('mr', 'Marathi'), ('(Manipuri)*', 'Meiteilon'), ('lus', 'Mizo*'), ('mn', 'Mongolian'), ('(Burmese)', 'Myanmar'), ('ne', 'Nepali'), ('no', 'Norwegian'), ('(Chichewa)', 'Nyanja'), ('(Oriya)', 'Odia'), ('om', 'Oromo*'), ('ps', 'Pashto'), ('fa', 'Persian'), ('pl', 'Polish'), ('(Portugal,', 'Portuguese'), ('pa', 'Punjabi'), ('qu', 'Quechua*'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sm', 'Samoan'), ('sa', 'Sanskrit*'), ('Gaelic', 'Scots'), ('nso', 'Sepedi*'), ('sr', 'Serbian'), ('st', 'Sesotho'), ('sn', 'Shona'), ('sd', 'Sindhi'), ('(Sinhalese)', 'Sinhala'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('so', 'Somali'), ('es', 'Spanish'), ('su', 'Sundanese'), ('sw', 'Swahili'), ('sv', 'Swedish'), ('(Filipino)', 'Tagalog'), ('tg', 'Tajik'), ('ta', 'Tamil'), ('tt', 'Tatar'), ('te', 'Telugu'), ('th', 'Thai'), ('ti', 'Tigrinya*'), ('ts', 'Tsonga*'), ('tr', 'Turkish'), ('tk', 'Turkmen'), ('(Akan)*', 'Twi'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('ug', 'Uyghur'), ('uz', 'Uzbek'), ('vi', 'Vietnamese'), ('cy', 'Welsh'), ('xh', 'Xhosa'), ('yi', 'Yiddish'), ('yo', 'Yoruba'), ('zu', 'Zulu'),

COUNT = ('Все слова', 'Все слова'), ('10', 10), ('50', 50), ('100', 100),


class ListForm(forms.Form):
    exact = forms.BooleanField(required=False, label='Точное совпадение')
    count = forms.ChoiceField(required=True, initial={'all': 'Все слова'}, choices=COUNT, label='')
    search = forms.CharField(label='')


class TranslateForm(forms.Form):
    from_lang = forms.ChoiceField(required=True, choices=LANGS, initial='en')
    from_translate = forms.CharField(required=True, label='Напишите слово или предложение',
                                     widget=forms.Textarea, min_length=1, max_length=5000
                                     )

    to_lang = forms.ChoiceField(required=True, choices=LANGS, initial='ru')
    to_translate = forms.CharField(required=True, label='Перевод', widget=forms.Textarea, disabled=True, )


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea)
    captcha = CaptchaField()
