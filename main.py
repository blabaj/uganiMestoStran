#!/usr/bin/env python

import os
import jinja2
import webapp2
import random


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)



def glavnoMesto(drzava):
    drzava = drzava.upper()
    drzave = {"SLOVENIJA" : "LJUBLJANA", "HRVASKA" : "ZAGREB", "SRBIJA" : "BEOGRAD", "ITALIJA" : "RIM"}

    if drzava in drzave.keys():
        glavnoMestoDrzave = drzave[drzava]
        return glavnoMestoDrzave
    else:
        napaka = "Drzave se ni v bazi"
        return napaka


def preveriMesto(drzava, mesto):
    drzava = drzava.upper()
    mesto = mesto.upper()
    mestoPrimerjava = glavnoMesto(drzava)
    if mesto == mestoPrimerjava:
        return "Drzi, mesto je pravilno!"

    else:
        return "Vpisano mesto ni glavno mesto te drzave!"


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        randomDrzava = random.randint(1,4)
        if (randomDrzava == 1):
            podatki = {"SLOVENIJA":"SLOVENIJA"}
            return self.render_template("uganiMesto.html",podatki)
        if (randomDrzava == 2):
            podatki = {"HRVASKA":"HRVASKA"}
            return self.render_template("uganiMesto.html",podatki)
        if (randomDrzava == 3):
            podatki = {"SRBIJA":"SRBIJA"}
            return self.render_template("uganiMesto.html",podatki)
        if (randomDrzava == 4):
            podatki = {"ITALIJA":"ITALIJA"}
            return self.render_template("uganiMesto.html",podatki)


    def post(self):
        mesto = self.request.get("mesto")
        drzava = self.request.get("drzava")
        print mesto,drzava
        zapis = preveriMesto(drzava,mesto)
        podatki = {"rezultat":zapis}
        print drzava
        return self.render_template("uganiMesto.html", podatki)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)