import requests
url = "https://esports.op.gg/matches/graphql"

def ban_rank_info(serieId: str, limit: int = 10, page: int = 0):
    """
    OP.GG E-Sports의 밴 순위 데이터 처리를 위해 호출되는 함수
    """
    try:
        query = """
query {
    pagedBanpicksBySerieId(serieId: "%s", limit: %d, page: %d) {
        bans{
            championId
            count
            currently
            previously
            rate
        }
    }
}
""" % (serieId, limit, page)
        headers = {
            "Content-Type": "application/json",
        }

        result = requests.post(url=url, json={"query": query}, headers=headers)

        if 200 <= result.status_code < 300:
            bans = result.json()['data']['pagedBanpicksBySerieId']

            if bans == []:
                return { "error": False, "code": "SUCCESS", "message": "밴 순위 데이터가 없습니다.", "data": None }

            return { "error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "data": bans }

        else:
            return { "error": True, "code": "NOTSENT", "message": f"서버와의 통신 과정 중 오류가 발생했습니다.\nStatus Code: {result.status_code}\nResponse: {result}", "data": None }

    except Exception as error:
        return { "error": True, "code": "UNKNOWN", "message": f"알 수 없는 에러가 발생했습니다.\n{error}", "data": None }
    
print(ban_rank_info("511"))
