# -*- coding: utf-8 -*-

import requests
url = "https://esports.op.gg/matches/graphql"


def series_tournaments_by_league_shortname(shortName: str):
    """
    OP.GG E-Sports에서 Series/Tournaments 정보를 불러올 때 호출되는 함수
    """
    try:
        query = """
query { 
    leagueByShortName(shortName: "%s") {
        shortName
        latestSerie{
            id
            tournaments{
                id
                name
                beginAt
                endAt
            }
            beginAt
            endAt
        }
    }
}""" % (shortName)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url=url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            series_tournaments = result.json()['data']['leagueByShortName']

            if series_tournaments == []:
                return { "error": False, "code": "SUCCESS", "message": "시리즈/토너먼트 데이터가 없습니다.", "data": None }

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": series_tournaments }

        else:
            return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }
