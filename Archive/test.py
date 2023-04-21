# -*- coding: utf-8 -*-

import requests
url = "https://esports.op.gg/matches/graphql"


def test_func(match_id: str, match_set: str):
    print(match_id, match_set)
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
        winner{
            id
            name
            acronym
            nationality
            imageUrl
        }
    }
}
""" % (match_id, match_set)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url=url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            recentMatches = result.json()['data']['gameByMatch']
            print(recentMatches)

        else:
            print(f"Status Code: {result.status_code}\nResponse: {result}")

    except Exception as error:
        print(error)

test_func("20517", "1")
