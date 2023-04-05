# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import opgg


def get_search_player(keyword: str):

    box_search_data = []
    player_id = ""
    player_nickName = ""
    search_key = ""

    if keyword == None: return None
    player_info = opgg.search_player(keyword=keyword)

    if player_info['error'] == False:
        for j in range(len(player_info['data'])):
            player_id = player_info['data'][j]['id']
            player_nickName = player_info['data'][j]['nickName']
            search_key = player_info['data'][j]['key']

            if search_key == "nickName":

                box_search_data.append({
                    "id": player_id,
                    "nickName": player_nickName
                })

    else:
        return box_search_data

    return box_search_data
