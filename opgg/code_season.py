# -*- coding: utf-8 -*-

import requests
url = "https://esports.op.gg/matches/graphql" # OP.GG Esports API URL


def season_info(tournamentId: str):
    """
    OP.GG Esports의 시즌 통계 데이터 처리를 위해 호출되는 함수
    """
    try:
        query = """
query {
    summary(tournamentId: "%s") {
        total
        baseStats{assists}
        baseStats{averageLength}
        baseStats{baronKills}
        baseStats{deaths}
        baseStats{dragonKills}
        baseStats{elderDragonKills}
        baseStats{heraldKills}
        baseStats{kills}
        baseStats{length}
        baseStats{maxLength}
        baseStats{minLength}
        baseStats{pentaKills}
        baseStats{towerKills}
    }
}
""" % (tournamentId)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            seasons = result.json()['data']['summary']

            if seasons == []:
                return { "error": False, "code": "SUCCESS", "message": "시즌 통계 데이터가 없습니다.", "data": None }

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": seasons }

        else:
            return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }


def ban_rank_info(serieId: str, limit: int = 10, page: int = 0):
    """
    OP.GG Esports의 밴 순위 데이터 처리를 위해 호출되는 함수
    """
    try:
        query = """
query {
    pagedBanpicksBySerieId(serieId: "%s", limit: %d, page: %d) {
        bans{championId}
        bans{count}
        bans{currently}
        bans{previously}
        bans{rate}
    }
}
""" % (serieId, limit, page)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            bans = result.json()['data']['pagedBanpicksBySerieId']

            if bans == []:
                return { "error": False, "code": "SUCCESS", "message": "밴 순위 데이터가 없습니다.", "data": None }

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": bans }

        else:
            return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }


def pick_rank_info(serieId: str, limit: int = 10, page: int = 0):
    """
    OP.GG Esports의 픽 순위 데이터 처리를 위해 호출되는 함수
    """
    try:
        query = """
query {
    pagedBanpicksBySerieId(serieId: "%s", limit: %d, page: %d) {
        picks{championId}
        picks{position}
        picks{count}
        picks{currently}
        picks{previously}
        picks{rate}
    }
}
""" % (serieId, limit, page)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            bans = result.json()['data']['pagedBanpicksBySerieId']

            if bans == []:
                return { "error": False, "code": "SUCCESS", "message": "픽 순위 데이터가 없습니다.", "data": None }

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": bans }

        else:
            return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }
