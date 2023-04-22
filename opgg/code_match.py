# -*- coding: utf-8 -*-

import requests
url = "https://esports.op.gg/matches/graphql" # OP.GG E-Sports API URL


def match_info_by_id(match_id: str):
    """
    OP.GG E-Sports에서 MatchID를 통한 경기 정보 데이터 처리를 위해 호출되는 함수
    """
    try:
        query = """
query {
    matchesByIds(ids: %s) {
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
""" % (match_id)
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


def game_info_by_id(match_id: str, match_set: str):
    """
    OP.GG E-Sports에서 MatchID와 MatchSet를 통한 경기 세부 정보 데이터 처리를 위해 호출되는 함수
    """
    try:
        query = """
query {
    gameByMatch(matchId: %s, set: %s) {
        id
        status
        finished
        beginAt
        endAt
        length
        detailedStats
        winner{
            id
            name
            acronym
            nationality
            imageUrl
        }
        teams{
            team{
                id
                name
                acronym
                nationality
                imageUrl
            }
            kills
            deaths
            assists
            side
            towerKills
            dragonKills
            elderDrakeKills
            baronKills
            inhibitorKills
            heraldKills
            goldEarned
            bans
        }
        players{
            player{
                id
                nickName
                position
                nationality
                imageUrl
            }
            team{
                id
                name
                acronym
                nationality
                imageUrl
            }
            side
            kills
            deaths
            assists
            championId
            spells
            runes{
                primary
                sub
            }
            items
            level
            creepScore
            goldEarned
            visionWardsBought
            totalDamageDealtToChampions
            totalDamageTaken
            doubleKills
            tripleKills
            quadraKills
            pentaKills
        }
    }
}
""" % (match_id, match_set)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url=url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            match_info = result.json()['data']['gameByMatch']

            if match_info == []:
                return { "error": False, "code": "SUCCESS", "message": "경기 데이터가 없습니다.", "data": None }

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": match_info }

        else:
            return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }


def match_started(match_id: str, tournament_id: str, status: str):
    """
    OP.GG E-Sports API에서 경기가 시작되었을 때 데이터 처리를 위해 호출되는 함수
    """
    try:
        if status != "not_started":
            return { "error": False, "code": "SUCCESS", "message": "조건에 맞지 않는 경기입니다.", "data": None }

        query = """
query {
    matchPreviewByTournament(id: "%s", tournamentId: "%s") {
        teamStats{
            team{
                id
                acronym
            }
            kills
            deaths
            assists
            winRate
            firstTower
            firstBaron
            firstBlood
            firstDragon
            goldEarned
        }
    }
}
""" % (match_id, tournament_id)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url=url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            matches = result.json()['data']['matchPreviewByTournament']

            if matches == []:
                return {"error": False, "code": "SUCCESS", "message": "경기 정보 데이터가 없습니다.", "data": None}

            return {"error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": matches}

        else:
            return {"error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None}

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }


def match_finished(league_id: str = "null", page: int = 0):
    """
    OP.GG E-Sports의 경기 종료 데이터 처리를 위해 호출되는 함수
    """
    try:
        query = """
query {
    pagedAllMatches(status: "finished", leagueId: %s, year: null, page: %d) {
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
        numberOfGames
        awayScore
        awayTeam{
            id
            name
            acronym
            nationality
            imageUrl
        }
        homeScore
        homeTeam{
            id
            name
            acronym
            nationality
            imageUrl
        }
        status
    }
}
""" % (league_id, page)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url=url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            matches = result.json()['data']['pagedAllMatches']

            if matches == []:
                return { "error": False, "code": "SUCCESS", "message": "경기 종료 데이터가 없습니다.", "data": None }

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": matches }

        else:
            return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }


def match_completed(match_info: dict):
    """
    OP.GG E-Sports API에서 경기 결과 데이터 처리를 위해 호출되는 함수

    - Input:
    {
        "matchId": "19972",
        "type": "complete",
        "set": 2,
        "title": "Semifinal 2: GEN vs DRX",
        "winner": "DRX",
        "winnerName": "DRX",
        "dpm": "GEN Ruler",
        "dtpm": "DRX Kingen",
        "gold": "DRX Deft",
        "cs": "DRX Zeka",
        "firstBlood": "GEN Ruler",
        "mvp": "DRX Zeka",
        "league": "Worlds"
    }

    - Output:
    {
        "error": False,
        "code": "SUCCESS",
        "message": "성공적으로 데이터를 불러왔습니다.",
        "data": {
            "team_1": "GEN",
            "team_2": "DRX",
            "match_id": "19972",
            "match_type": "complete",
            "match_set": "2",
            "match_title": "GEN vs DRX (Worlds)",
            "match_winner_name": "DRX",
            "match_winner_shortName": "DRX",
            "match_league": "Worlds",
            "dpm": "GEN Ruler",
            "dtpm": "DRX Kingen",
            "gold": "DRX Deft",
            "cs": "DRX Zeka",
            "firstBlood": "GEN Ruler",
            "mvp": "DRX Zeka"
        }
    }
    """
    try:
        match = match_info

        if match == None or match == "" or match == {} or match == []:
            return { "error": True, "code": "NOINPUT", "message": "호출된 함수에 대입할 데이터가 없습니다.", "data": None }
        elif match['type'] != "complete":
            return { "error": True, "code": "NOCOMPLETE", "message": "호출된 함수에 대입된 데이터가 경기 종료 데이터가 아닙니다.", "data": None }
        elif match['type'] == "complete":

            if match['dpm'] == "": match['dpm'] = "-"
            if match['dtpm'] == "": match['dtpm'] = "-"
            if match['gold'] == "": match['gold'] = "-"
            if match['cs'] == "": match['cs'] = "-"
            if match['firstBlood'] == "": match['firstBlood'] = "-"
            if match['mvp'] == "": match['mvp'] = "-"

            try: match_name = match['title'].split(': ')[1]
            except: match_name = match['title']
            msg_team_1 = match_name.split(' vs ')[0]
            msg_team_2 = match_name.split(' vs ')[1]
            msg_match_id = match['matchId']
            msg_match_type = match['type']
            msg_match_set = match['set']
            msg_match_title = f"{match_name} ({match['league']})"
            msg_winner_name = match['winnerName']
            msg_winner_shortName = match['winner']
            msg_league = match['league']
            msg_dpm = match['dpm']
            msg_dtpm = match['dtpm']
            msg_gold = match['gold']
            msg_cs = match['cs']
            msg_firstBlood = match['firstBlood']
            msg_mvp = match['mvp']

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": { "team_1": msg_team_1, "team_2": msg_team_2, "match_id": msg_match_id, "match_type": msg_match_type, "match_set": msg_match_set, "match_title": msg_match_title, "match_winner_name": msg_winner_name, "match_winner_shortName": msg_winner_shortName, "match_league": msg_league, "dpm": msg_dpm, "dtpm": msg_dtpm, "gold": msg_gold, "cs": msg_cs, "firstBlood": msg_firstBlood, "mvp": msg_mvp } }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }
