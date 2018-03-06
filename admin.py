import json
from urllib.request import urlopen
import urllib.parse

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout

def loaddata():
    data = urlopen('http://localhost:8090/getfeasts').read()
    data = json.loads(data.decode('utf-8'))
    titles = []
    for i in range(len(data['feasts'])):
        titles.append('{} - {}'.format(i, data['feasts'][i]['feast']))
    return data['feasts'], titles

class YearFeastsForm(GridLayout):
    feasts, titles = loaddata()
    feasts_spr = ObjectProperty()
    detail_txt = ObjectProperty()
    i = -1

    def showdetail(self, text):
        if text != '':
            self.i = int(text.split('-')[0].strip())
            date = self.feasts[self.i]
            self.detail_txt.text = '''- Feast: {}
- Date: {}
- Tradition: {}
- Origines: {}'''.format(date['feast'], date['date'],
                            date['tradition'], date['origins'])

    def delete(self):
        data = urlopen('http://localhost:9090/deletefeast?i=' + str(self.i))
        data = data.read().decode('utf-8')
        if (data == 'OK'):
            self.detail_txt.text = ''
            self.feasts_spr.text = ''
            self.feasts, self.feasts_spr.values = loaddata()
    #
    def add(self):
        self.feast = self.feast_txt.text
        self.date = self.date_txt.text
        self.tradition = self.tradition_txt.text
        self.origin = self.origins_txt.text
        params = {
            'feast': self.feast,
            'date': self.date,
            'tradition': self.tradition,
            'origin': self.origin
        }
        urlopen('http://localhost:8090/addfeast?' + urllib.parse.urlencode(params))



class YearFeastsApp(App):
    title = 'YearFeasts'

YearFeastsApp().run()
