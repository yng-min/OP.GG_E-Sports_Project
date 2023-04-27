# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import opgg


def get_bans_info(serieId: str, limit: int = 10, page: int = 0):

    box_bans = []
    champion_id = ""
    count = 0
    currently = 0
    previously = 0
    rate = 0.00

    if serieId == None: return None
    bans_info = opgg.ban_rank_info(serieId=serieId, limit=limit, page=page)

    if bans_info['error'] == False:
        for i in range(len(bans_info['data']['bans'])):
            champion_id = bans_info['data']['bans'][i]['championId']
            count = bans_info['data']['bans'][i]['count']
            currently = bans_info['data']['bans'][i]['currently']
            previously = bans_info['data']['bans'][i]['previously']
            rate = (bans_info['data']['bans'][i]['rate'] * 100).__round__(2)

            box_bans.append({
                "id": champion_id,
                "count": count,
                "currently": currently,
                "previously": previously,
                "rate": rate
            })

    else:
        return bans_info

    return box_bans


def get_picks_info(serieId: str, limit: int = 10, page: int = 0):

    box_picks = []
    champion_id = ""
    count = 0
    currently = 0
    previously = 0
    rate = 0.00

    if serieId == None: return None
    picks_info = opgg.pick_rank_info(serieId=serieId, limit=limit, page=page)

    if picks_info['error'] == False:
        for i in range(len(picks_info['data']['picks'])):
            champion_id = picks_info['data']['picks'][i]['championId']
            count = picks_info['data']['picks'][i]['count']
            currently = picks_info['data']['picks'][i]['currently']
            previously = picks_info['data']['picks'][i]['previously']
            rate = (picks_info['data']['picks'][i]['rate'] * 100).__round__(2)

            box_picks.append({
                "id": champion_id,
                "count": count,
                "currently": currently,
                "previously": previously,
                "rate": rate
            })

    else:
        return picks_info

    return box_picks
