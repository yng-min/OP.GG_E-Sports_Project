# -*- coding: utf-8 -*-

import requests
url = "https://esports.op.gg/matches/graphql"


def player_info_by_nickname(playerNickname: str):
    print(playerNickname)
    try:
        query = """
query {
    playerByNickname(nickName: "%s") {
        id
    }
""" % (playerNickname)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url=url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            player = result.json()['data']['playerByNickname']
            print(player)

        else:
            print(f"Status Code: {result.status_code}\nResponse: {result}")

    except Exception as error:
        print(error)

player_info_by_nickname("Faker")
