# -*- coding: utf-8 -*-

import requests
url = "https://esports.op.gg/matches/graphql" # OP.GG E-Sports API URL


def match_info_by_id(matchId: str):
    """
    OP.GG E-Sports에서 MatchID를 통한 경기 정보 데이터 처리를 위해 호출되는 함수
    """
    try:
        query = """
query {
    matchesByIds(ids: [%s]) {
        id
        name
        originalScheduledAt
        scheduledAt
        beginAt
        endAt
        status
        numberOfGames
        liveSupported
        liveOpensAt
        streams{
            isMain
            isOfficial
            rawUrl
        }
        homeTeam{
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
        awayTeam{
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
        ranks{
            homeTeamRank{
                position
                previously
                point
                setWin
                setLose
                win
                lose
            }
            awayTeamRank{
                position
                previously
                point
                setWin
                setLose
                win
                lose
            }
        }
    }
}
""" % (matchId)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url=url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            match_info = result.json()['data']['matchesByIds']

            if match_info == []:
                return { "error": False, "code": "SUCCESS", "message": "경기 데이터가 없습니다.", "data": None }

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": match_info }

        else:
            return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }
    

print(match_info_by_id("21473"))
