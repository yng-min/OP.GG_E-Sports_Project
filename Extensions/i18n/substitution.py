# -*- coding: utf-8 -*-

class Substitution:

    def substitution(ctx):
        language = None

        import json
        try:
            with open(r"./Languages/en.json", "rt", encoding="UTF8") as enJson:
                en = json.load(enJson)
        except: print("en.json이 로드되지 않음")

        try:
            with open(r"./Languages/ko.json", "rt", encoding="UTF8") as koJson:
                ko = json.load(koJson)
        except: print("ko.json이 로드되지 않음")

        if ctx.locale == "en":
            language = en
        elif ctx.locale == "ko":
            language = ko
        else:
            language = en

        return language
