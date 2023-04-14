# -*- coding: utf-8 -*-

import requests
url = "https://esports.op.gg/matches/graphql" # OP.GG E-Sports API URL


def league_standing(tournamentId: str):
    """
    OP.GG E-Sports의 리그 순위 데이터 처리를 위해 호출되는 함수
    """
    try:
        query = """
query {
    standings(tournamentId: "%s") {
        position
        previously
        point
        win
        lose
        setWin
        setLose
        team{
            id
            name
            acronym
            nationality
            foundedAt
            imageUrl
            youtube
            twitter
            instagram
            facebook
            discord
            website
        }
        recentMatches{
            id
            tournamentId
        }
    }
}
""" % tournamentId
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url=url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            teams = result.json()['data']['standings']

            if teams == []:
                return { "error": False, "code": "SUCCESS", "message": "리그 순위 데이터가 없습니다.", "data": None }

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": teams }

        else:
            return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }


def player_mvp_rank(tournamentId: str, limit: int = 10, page: int = 0):
    """
    OP.GG E-Sports의 선수 랭킹 데이터 처리를 위해 호출되는 함수
    """
    try:
        query = """
query {
    pagedMvpRankByTournament(tournamentId: "%s", limit: %d, page: %d) {
        mvps{
            player{
                id
                nickName
                nationality
                imageUrl
            }
            team{
                id
                name
                acronym
                nationality
            }
            position
            currently
            previously
            mvpPoint
            games
            kda
            kills
            deaths
            assists
            tournamentId
        }
    }
}
""" % (tournamentId, limit, page)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url=url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            mvps = result.json()['data']['pagedMvpRankByTournament']

            if mvps == []:
                return { "error": False, "code": "SUCCESS", "message": "밴 순위 데이터가 없습니다.", "data": None }

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": mvps }

        else:
            return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }
