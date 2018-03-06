import json
import os
import cherrypy
from cherrypy.lib.static import serve_file
import jinja2
import jinja2plugin
import jinja2tool

class WebApp():

    def __init__(self):
        self.feasts= self.loadfeasts()

    #route vers la page d'accueil
    @cherrypy.expose
    def index(self):
        if len(self.feasts) == 0:
            feasts = '<p>Base de donnée vide.</p>'
        else:
            feasts = '<table id="feasts">'
            for i in range(len(self.feasts)):
                liste = self.feasts[i]
                feasts += '''<tr>
                    <th>
                    <a href="loadinfos?i={}">{}</a>
                    </th>
                </tr>'''.format(i, liste['feast'])
            feasts += '</table>'
        return {'feasts': feasts}

    #route vers l'ajout de date
    @cherrypy.expose
    def add(self):
        return serve_file(os.path.join(ROOT, 'templates/add.html'))

    #chargement des fêtes
    def loadfeasts(self):
        try:
            with open('Bdd.json', 'r', encoding="utf-8") as file:
                content = json.loads(file.read(), encoding="utf-8")
                return content['feasts']
        except:
            cherrypy.log('Loading database failed.')
            return []

    #route vers les infos des fêtes
    @cherrypy.expose
    def loadinfos(self,i):
        liste= self.feasts[int(i)]
        return {'feast': liste['feast'], 'date': liste['date'], 'tradition': liste['tradition'], 'origins': liste['origins']}

    #route vers ajout d'evenement dans la base donnée
    @cherrypy.expose
    def addevent(self, feast, date, tradition,origins):
        if feast != '' and date != '':
            self.feasts.append({
                'feast': feast,
                'date': date,
                'tradition': tradition,
                'origins': origins
            })
            self.savevent()
        raise cherrypy.HTTPRedirect('/')

    #sauvegarde des ajouts dans la base donnée
    def savevent(self):
        try:
            with open('Bdd.json', 'w', encoding="utf-8") as file:
                file.write(json.dumps({
                    'feasts': self.feasts
                }, ensure_ascii=False))
        except:
            cherrypy.log('Saving database failed.')

    @cherrypy.expose
    def getfeasts(self):
        return json.dumps({
            'feasts': self.feasts
        }, ensure_ascii=False).encode('utf-8')

    #route pour ajouter une fête via kivy
    @cherrypy.expose
    def deletefeast(self, i):
        result = 'KO'
        i = int(i)
        if 0 <= i < len(self.feasts):
            del(self.feasts[i])
            result = 'OK'
        return result.encode('utf-8')

    #route pour ajouter une fête via kivy
    @cherrypy.expose
    def addfeast(self,feast,date,tradition,origin):
        self.feasts.append(
                {
                    'tradition':str(tradition),
                    'feast':str(feast),
                    'origins':str(origin),
                    'date':str(date)
                }
        )
        self.savevent()



if __name__ == '__main__':
    # Register Jinja2 plugin and tool
    ENV = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
    jinja2plugin.Jinja2TemplatePlugin(cherrypy.engine, env=ENV).subscribe()
    cherrypy.tools.template = jinja2tool.Jinja2Tool()

    ROOT = os.path.abspath(os.getcwd())
    cherrypy.quickstart(WebApp(), '', 'Projet_info.conf')
