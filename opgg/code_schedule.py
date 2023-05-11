# -*- coding: utf-8 -*-

import requests
import datetime
import pytz
url = "https://esports.op.gg/matches/graphql" # OP.GG E-Sports API URL


def load_schedule(date: str = "null"):
    """
    OP.GG E-Sports의 경기 일정 데이터 처리를 위해 호출되는 함수
    """
    try:
        if date == "null": date = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")
        query = """
query {
    upcomingMatchesByDate(date: "%s") {
        id
        tournamentId
        tournament{
            serie{
                league{
                    shortName
                }
            }
        }
        name
        originalScheduledAt
        scheduledAt
        status
        homeTeam{
            id
            name
            acronym
            nationality
            foundedAt
            imageUrl
        }
        awayTeam{
            id
            name
            acronym
            nationality
            foundedAt
            imageUrl
        }
    }
}
""" % (date)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url=url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            matches = result.json()['data']['upcomingMatchesByDate']

            if matches == []:
                return { "error": False, "code": "SUCCESS", "message": "경기 일정 데이터가 없습니다.", "data": None }

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": matches }

        else:
            return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }


def save_schedule(leagueId: str = "null", page: int = 0):
    """
    OP.GG E-Sports의 경기 일정 데이터 저장을 위해 호출되는 함수
    """
    try:
        now_year = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y")
        now_month = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("X%m").replace("X0", "X").replace("X", "")
        query = """
query {
    pagedAllMatches(status: "not_started", leagueId: %s, year: %s, month: %s, page: %d) {
        id
        tournamentId
        tournament{
            serie{
                league{
                    shortName
                }
            }
        }
        name
        originalScheduledAt
        scheduledAt
        numberOfGames
        status
        homeTeam{
            id
            name
            acronym
            nationality
            foundedAt
            imageUrl
        }
        awayTeam{
            id
            name
            acronym
            nationality
            foundedAt
            imageUrl
        }
    }
}
""" % (leagueId, now_year, now_month, page)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url=url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            matches = result.json()['data']['pagedAllMatches']

            if matches == []:
                return { "error": False, "code": "SUCCESS", "message": "경기 일정 데이터가 없습니다.", "data": None }

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": matches }

        else:
            return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }


def update_schedule(matchInfo: str): # null(js) -> None(py) 문법 변환을 위해 dict 대신 str로 받음
    """
    OP.GG E-Sports API에서 경기 일정이 업데이트 되었을 때 데이터 처리를 위해 호출되는 함수

    - Input:
    {
        "matchId": "20014",
        "type": "reschedule",
        "scheduledAt": "2022-10-03T07:00:00.000Z",
        "originalScheduledAt": "2022-10-03T06:00:00.000Z",
        "title": "Tiebreaker: LLL vs TBD",
        "league": "Worlds"
    }

    - Output:
    {
        "error": False,
        "code": "SUCCESS",
        "message": "성공적으로 데이터를 불러왔습니다.",
        "data": {
            "team_1": "LLL",
            "team_2": "TBD",
            "match_id": "20014",
            "match_type": "reschedule",
            "match_title": "LLL vs TBD",
            "match_league": "Worlds",
            "match_scheduledAt": "2022-10-03T07:00:00.000Z",
            "match_originalScheduledAt": "2022-10-03T06:00:00.000Z"
        }
    }
    """
    try:
        # null(js) -> None(py) 문법 변환 작업 *데이터 자체는 OP.GG E-Sports API에서 직접 다이렉트로 보내주기 때문에 eval문 보안 이슈 X*
        match = str(matchInfo).replace("null", "None")
        match = eval(match)

        if match == None or match == "" or match == {} or match == []:
            return { "error": True, "code": "NOINPUT", "message": "호출된 함수에 대입할 데이터가 없습니다.", "data": None }
        elif match['type'] != "reschedule":
            return { "error": True, "code": "NOCOMPLETE", "message": "호출된 함수에 대입된 데이터가 일정 변경 데이터가 아닙니다.", "data": None }
        elif match['type'] == "reschedule":

            try: match_name = match['title'].split(': ')[1]
            except: match_name = match['title']
            msg_team_1 = match_name.split(' vs ')[0]
            msg_team_2 = match_name.split(' vs ')[1]
            msg_match_id = match['matchId']
            msg_match_type = match['type']
            msg_match_title = f"{match_name} ({match['league']})"
            msg_league = match['league']
            msg_scheduledAt = match['scheduledAt']
            msg_originalScheduledAt = match['originalScheduledAt']

            return {"error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": { "team_1": msg_team_1, "team_2": msg_team_2, "match_id": msg_match_id, "match_type": msg_match_type, "match_title": msg_match_title, "match_league": msg_league, "match_scheduledAt": msg_scheduledAt, "match_originalScheduledAt": msg_originalScheduledAt } }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }
