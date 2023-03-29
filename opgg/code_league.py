# -*- coding: utf-8 -*-

import requests
url = "https://esports.op.gg/matches/graphql" # OP.GG Esports API URL


def league_standing(tournamentId: str):
    """
    OP.GG Esports의 리그 순위 데이터 처리를 위해 호출되는 함수
    """
    try:
        query = """
query {
    standings(tournamentId: "%s") {
        position
        previously
        setWin
        setLose
        team{id}
        team{name}
        team{acronym}
        team{nationality}
        team{foundedAt}
        team{imageUrl}
        team{youtube}
        team{twitter}
        team{instagram}
        team{facebook}
        team{website}
        recentMatches{id}
        recentMatches{tournamentId}
    }
}
""" % tournamentId
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            teams = result.json()['data']['standings']

            if teams == []:
                return { "error": False, "code": "SUCCESS", "message": "리그 순위 데이터가 없습니다.", "data": None }

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": teams }

        else:
            return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }


def player_info_by_team(tournamentId: str, teamId: str):
    """
    OP.GG Esports의 팀에서 선수 정보 데이터 처리를 위해 호출되는 함수
    """
    try:
        query = """
query {
    playersByTournamentAndTeam(tournamentId: "%s", teamId: "%s") {
        player{id}
        player{nickName}
        player{firstName}
        player{lastName}
        player{position}
        player{nationality}
        player{imageUrl}
        player{birthday}
        player{stream}
        player{youtube}
        player{twitter}
        player{instagram}
        player{facebook}
        player{discord}
        playerStat{games}
        playerStat{winRate}
        playerStat{wins}
        playerStat{loses}
        playerStat{kills}
        playerStat{deaths}
        playerStat{assists}
        playerStat{kda}
        playerStat{dpm}
        playerStat{dtpm}
        playerStat{gpm}
        playerStat{cspm}
        playerStat{dpgr}
        playerStat{firstBlood}
        playerStat{firstTower}
        playerStat{wardsPlaced}
        playerStat{wardsKilled}
    }
}
""" % (tournamentId, teamId)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            players = result.json()['data']['playersByTournamentAndTeam']

            if players == []:
                return { "error": False, "code": "SUCCESS", "message": "선수 정보 데이터가 없습니다.", "data": None }

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": players }

        else:
            return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }


def player_info(playerId: list):
    """
    OP.GG Esports의 선수 정보 데이터 처리를 위해 호출되는 함수
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
    }
}
""" % (playerIds)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            player = result.json()['data']['playersByIds']

            if player == []:
                return { "error": False, "code": "SUCCESS", "message": "선수 정보 데이터가 없습니다.", "data": None }

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": player }

        else:
            return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }


def player_mvp_rank(tournamentId: str, limit: int = 10, page: int = 0):
    """
    OP.GG Esports의 선수 랭킹 데이터 처리를 위해 호출되는 함수
    """
    try:
        query = """
query {
    pagedMvpRankByTournament(tournamentId: "%s", limit: %d, page: %d) {
        mvps{player{id}}
        mvps{player{nickName}}
        mvps{player{nationality}}
        mvps{player{imageUrl}}
        mvps{team{id}}
        mvps{team{name}}
        mvps{team{acronym}}
        mvps{team{nationality}}
        mvps{position}
        mvps{currently}
        mvps{previously}
        mvps{mvpPoint}
        mvps{games}
        mvps{kda}
        mvps{kills}
        mvps{deaths}
        mvps{assists}
    }
}
""" % (tournamentId, limit, page)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            mvps = result.json()['data']['pagedMvpRankByTournament']

            if mvps == []:
                return { "error": False, "code": "SUCCESS", "message": "밴 순위 데이터가 없습니다.", "data": None }

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": mvps }

        else:
            return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }
