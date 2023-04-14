# -*- coding: utf-8 -*-

import requests
url = "https://esports.op.gg/matches/graphql" # OP.GG E-Sports API URL


def search_player(keyword: str):
    """
    OP.GG E-Sports의 선수 검색 데이터 처리를 위해 호출되는 함수
    """
    try:
        query = """
query {
    playerByNickname(nickName: "%s") {
        id
        nickName
        currentTeam{
            acronym
        }
    }
}
""" % (keyword)
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


# def search_player(keyword: str):
#     """
#     OP.GG E-Sports의 선수 검색 데이터 처리를 위해 호출되는 함수
#     """
#     try:
#         query = """
# query {
#     search(keyword: "%s") {
#         matches{
#             key
#             value
#         }
#     }
# }
# """ % keyword # item의 id와 nickName을 가져와야 함
#         headers = {
#             "Content-Type": "application/json",
#         }

#         result = requests.post(url=url, json={"query": query}, headers=headers)

#         if 200 <= result.status_code < 300:
#             items = result.json()['data']['search']

#             if items == []:
#                 return { "error": False, "code": "SUCCESS", "message": "선수 검색 데이터가 없습니다.", "data": None }

#             return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": items }

#         else:
#             return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

#     except Exception as error:
#         return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }
