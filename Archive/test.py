# -*- coding: utf-8 -*-

import requests
url = "https://esports.op.gg/matches/graphql"


def recentMatchesByPlayerId(playerId: str):
    print(playerId)
    try:
        query = """
query {
    player(playerId: "%s") {
        currentTeam{
            recentMatches{
                beginAt
                name
                id
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
            recentMatches = result.json()['data']['player']['currentTeam']['recentMatches']
            print(recentMatches)

        else:
            print(f"Status Code: {result.status_code}\nResponse: {result}")

    except Exception as error:
        print(error)

recentMatchesByPlayerId("1836")
