# -*- coding: utf-8 -*-

import requests
url = "https://esports.op.gg/matches/graphql" # OP.GG E-Sports API URL


def player_info_by_id(playerId: list):
    """
    OP.GG E-Sports의 선수 ID를 통한 선수 정보 데이터 처리를 위해 호출되는 함수
    """
    try:
        playerIds = ""
        for i in playerId: playerIds += f"{i}, "
        playerIds = playerIds[:-2]
        query = """
query {
    playersByIds(playerIds: [%s]) {
        id
        nickName
        firstName
        lastName
        position
        nationality
        imageUrl
        birthday
        stream
        youtube
        twitter
        instagram
        facebook
        discord
        currentTeam{
            id
            name
            acronym
            nationality
            imageUrl
        }
    }
}
""" % (playerIds)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url=url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            player = result.json()['data']['playersByIds']

            if player == []:
                return { "error": False, "code": "SUCCESS", "message": "선수 정보 데이터가 없습니다.", "data": None }

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": player }

        else:
            return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }


def player_info_by_nickname(playerNickname: str):
    """
    OP.GG E-Sports의 선수 닉네임을 통한 선수 정보 데이터 처리를 위해 호출되는 함수
    """
    try:
        query = """
query {
    playerByNickname(nickName: "%s") {
        id
        nickName
        firstName
        lastName
        position
        nationality
        imageUrl
        birthday
        stream
        youtube
        twitter
        instagram
        facebook
        discord
        currentTeam{
            id
            name
            acronym
            nationality
            imageUrl
        }
    }
}
""" % (playerNickname)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url=url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            player = result.json()['data']['playerByNickname']

            if player == []:
                return { "error": False, "code": "SUCCESS", "message": "선수 정보 데이터가 없습니다.", "data": None }

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": player }

        else:
            return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }


def players_info_by_team_id(tournamentId: str, teamId: str):
    """
    OP.GG E-Sports의 팀에서 선수 정보 데이터 처리를 위해 호출되는 함수
    """
    try:
        query = """
query {
    playersByTournamentAndTeam(tournamentId: "%s", teamId: "%s") {
        player{
            id
            nickName
            firstName
            lastName
            position
            nationality
            imageUrl
            birthday
            stream
            youtube
            twitter
            instagram
            facebook
            discord
        }
        playerStat{
            team{
                id
                name
                acronym
                nationality
                imageUrl
            }
            games
            winRate
            wins
            loses
            kills
            deaths
            assists
            kda
            dpm
            dtpm
            gpm
            cspm
            dpgr
            firstBlood
            firstTower
            wardsPlaced
            wardsKilled
        }
    }
}
""" % (tournamentId, teamId)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url=url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            players = result.json()['data']['playersByTournamentAndTeam']

            if players == []:
                return { "error": False, "code": "SUCCESS", "message": "선수 정보 데이터가 없습니다.", "data": None }

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": players }

        else:
            return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }


def recent_matches_by_id(playerId: str):
    """
    OP.GG E-Sports 선수의 최근 5경기 정보 데이터 처리를 위해 호출되는 함수
    """
    try:
        query = """
query {
    player(playerId: "%s") {
        currentTeam{
            recentMatches{
                id
                name
                beginAt
                winnerTeam{
                    id
                    name
                    acronym
                }
            }
        }
    }
}
""" % (playerId)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url=url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            recentMatches = result.json()['data']['player']

            if recentMatches == []:
                return { "error": False, "code": "SUCCESS", "message": "최근 경기 데이터가 없습니다.", "data": None }

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": recentMatches }

        else:
            return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }
