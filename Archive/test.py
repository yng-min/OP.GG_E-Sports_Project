# -*- coding: utf-8 -*-

import requests
url = "https://esports.op.gg/matches/graphql"


def team_info_by_name(teamName: str):
    print(teamName)
    try:
        query = """
query {
    TeamByName(team: "%s") {
        id
    }
}
""" % (teamName)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url=url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            team = result.json()['data']['TeamByName']
            print(team)

        else:
            print(f"Status Code: {result.status_code}\nResponse: {result}")

    except Exception as error:
        print(error)

team_info_by_name("T1")
