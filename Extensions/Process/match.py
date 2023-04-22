# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import opgg


def get_recentMatches(recentMatches):

    box_recentMatches = {}
    match_id = ""
    match_name = ""
    match_originalScheduledAt = ""
    match_scheduledAt = ""
    match_beginAt = ""
    match_endAt = ""
    match_status = ""
    match_numberOfGames = ""
    match_liveSupported = ""
    match_liveOpensAt = ""
    match_streams = ""
    match_winnerTeam = ""
    match_homeTeam = ""
    match_homeScore = ""
    match_awayTeam = ""
    match_awayScore = ""
    match_ranks = ""

    for i in range(len(recentMatches)):
        match_info = opgg.match_info_by_id(match_id=recentMatches[i]['id'])

        match_id = match_info['data'][0]['id']
        match_name = match_info['data'][0]['name']
        match_originalScheduledAt = match_info['data'][0]['originalScheduledAt']
        match_scheduledAt = match_info['data'][0]['scheduledAt']
        match_beginAt = match_info['data'][0]['beginAt']
        match_endAt = match_info['data'][0]['endAt']
        match_status = match_info['data'][0]['status']
        match_numberOfGames = match_info['data'][0]['numberOfGames']
        match_liveSupported = match_info['data'][0]['liveSupported']
        match_liveOpensAt = match_info['data'][0]['liveOpensAt']
        match_streams = match_info['data'][0]['streams']
        match_winnerTeam = match_info['data'][0]['winnerTeam']
        match_homeTeam = match_info['data'][0]['homeTeam']
        match_homeScore = match_info['data'][0]['homeScore']
        match_awayTeam = match_info['data'][0]['awayTeam']
        match_awayScore = match_info['data'][0]['awayScore']
        match_ranks = match_info['data'][0]['ranks']

        box_recentMatches[match_id] = {
            "id": match_id,
            "name": match_name,
            "originalScheduledAt": match_originalScheduledAt,
            "scheduledAt": match_scheduledAt,
            "beginAt": match_beginAt,
            "endAt": match_endAt,
            "status": match_status,
            "numberOfGames": match_numberOfGames,
            "liveSupported": match_liveSupported,
            "liveOpensAt": match_liveOpensAt,
            "streams": match_streams,
            "winnerTeam": match_winnerTeam,
            "homeTeam": match_homeTeam,
            "homeScore": match_homeScore,
            "awayTeam": match_awayTeam,
            "awayScore": match_awayScore,
            "ranks": match_ranks
        }

    return box_recentMatches


def get_game_info_by_id(match_id, match_set):

    box_game_info = {}
    box_team = []
    team_templete = {}
    team_check_blue = False
    team_check_red = False
    box_player = []
    player_templete = {}
    player_check_top_blue = False
    player_check_jun_blue = False
    player_check_mid_blue = False
    player_check_adc_blue = False
    player_check_sup_blue = False
    player_check_top_red = False
    player_check_jun_red = False
    player_check_mid_red = False
    player_check_adc_red = False
    player_check_sup_red = False
    game_id = ""
    game_status = ""
    game_finished = False
    game_beginAt = ""
    game_endAt = ""
    game_length = 0
    game_detailedStats = False
    game_winner_id = ""
    game_winner_name = ""
    game_winner_acronym = ""
    game_winner_nationality = ""
    game_winner_imageUrl = ""
    game_team_id = ""
    game_team_name = ""
    game_team_acronym = ""
    game_team_nationality = ""
    game_team_imageUrl = ""
    game_team_kills = 0
    game_team_deaths = 0
    game_team_assists = 0
    game_team_side = ""
    game_team_towerKills = 0
    game_team_dragonKills = 0
    game_team_elderDrakeKills = 0
    game_team_baronKills = 0
    game_team_inhibitorKills = 0
    game_team_heraldKills = 0
    game_team_goldEarned = 0
    game_team_bans = []
    game_player_id = ""
    game_player_nickName = ""
    game_player_position = ""
    game_player_nationality = ""
    game_player_imageUrl = ""
    game_player_team_id = ""
    game_player_team_name = ""
    game_player_team_acronym = ""
    game_player_team_nationality = ""
    game_player_team_imageUrl = ""
    game_player_side = ""
    game_player_kills = 0
    game_player_deaths = 0
    game_player_assists = 0
    game_player_kda = ""
    game_player_championId = ""
    game_player_spells = []
    game_player_runes_primary = []
    game_player_runes_sub = []
    game_player_items = []
    game_player_level = 0
    game_player_creepScore = 0
    game_player_goldEarned = 0
    game_player_visionWardsBought = 0
    game_player_totalDamageDealtToChampions = 0
    game_player_totalDamageTaken = 0
    game_player_doubleKills = False
    game_player_tripleKills = False
    game_player_quadraKills = False
    game_player_pentaKills = False

    game_info = opgg.game_info_by_id(match_id=match_id, match_set=match_set)

    if game_info['error'] == False:
        game_id = game_info['data']['id']
        game_status = game_info['data']['status']
        game_finished = game_info['data']['finished']
        game_beginAt = game_info['data']['beginAt']
        game_endAt = game_info['data']['endAt']
        game_length = game_info['data']['length']
        game_detailedStats = game_info['data']['detailedStats']

        game_winner_id = game_info['data']['winner']['id']
        game_winner_name = game_info['data']['winner']['name']
        game_winner_acronym = game_info['data']['winner']['acronym']
        game_winner_nationality = game_info['data']['winner']['nationality']
        game_winner_imageUrl = game_info['data']['winner']['imageUrl']

        for z in range(len(game_info['data']['teams'])):
            for i in range(len(game_info['data']['teams'])):
                game_team_id = game_info['data']['teams'][i]['team']['id']
                game_team_name = game_info['data']['teams'][i]['team']['name']
                game_team_acronym = game_info['data']['teams'][i]['team']['acronym']
                game_team_nationality = game_info['data']['teams'][i]['team']['nationality']
                game_team_imageUrl = game_info['data']['teams'][i]['team']['imageUrl']
                game_team_kills = game_info['data']['teams'][i]['kills']
                game_team_deaths = game_info['data']['teams'][i]['deaths']
                game_team_assists = game_info['data']['teams'][i]['assists']
                game_team_side = game_info['data']['teams'][i]['side'].replace("blue", "블루").replace("red", "레드")
                game_team_towerKills = game_info['data']['teams'][i]['towerKills']
                game_team_dragonKills = game_info['data']['teams'][i]['dragonKills']
                game_team_elderDrakeKills = game_info['data']['teams'][i]['elderDrakeKills']
                game_team_baronKills = game_info['data']['teams'][i]['baronKills']
                game_team_inhibitorKills = game_info['data']['teams'][i]['inhibitorKills']
                game_team_heraldKills = game_info['data']['teams'][i]['heraldKills']
                game_team_goldEarned = game_info['data']['teams'][i]['goldEarned']
                game_team_bans = game_info['data']['teams'][i]['bans']

                team_templete = {
                    "id": game_team_id,
                    "name": game_team_name,
                    "acronym": game_team_acronym,
                    "nationalty": game_team_nationality,
                    "imageUrl": game_team_imageUrl,
                    "kills": game_team_kills,
                    "deaths": game_team_deaths,
                    "assists": game_team_assists,
                    "side": game_team_side,
                    "towerKills": game_team_towerKills,
                    "dragonKills": game_team_dragonKills,
                    "elderDrakeKills": game_team_elderDrakeKills,
                    "baronKills": game_team_baronKills,
                    "inhibitorKills": game_team_inhibitorKills,
                    "heraldKills": game_team_heraldKills,
                    "goldEarned": game_team_goldEarned,
                    "bans": game_team_bans
                }

                # 팀 진영 순서 정렬(블루팀, 레드팀 순)
                if (game_team_side == "블루") and (team_check_blue == False):
                    box_team.append(team_templete)
                    team_check_blue = True
                if (game_team_side == "레드") and (team_check_blue == True) and (team_check_red == False):
                    box_team.append(team_templete)
                    team_check_red = True

        for x in range(len(game_info['data']['players'])):
            for j in range(len(game_info['data']['players'])):
                game_player_id = game_info['data']['players'][j]['player']['id']
                game_player_nickName = game_info['data']['players'][j]['player']['nickName']
                game_player_position = game_info['data']['players'][j]['player']['position'].replace("top", "탑").replace("jun", "정글").replace("mid", "미드").replace("adc", "원딜").replace("sup", "서포터")
                game_player_nationality = game_info['data']['players'][j]['player']['nationality']
                game_player_imageUrl = game_info['data']['players'][j]['player']['imageUrl']
                game_player_team_id = game_info['data']['players'][j]['team']['id']
                game_player_team_name = game_info['data']['players'][j]['team']['name']
                game_player_team_acronym = game_info['data']['players'][j]['team']['acronym']
                game_player_team_nationality = game_info['data']['players'][j]['team']['nationality']
                game_player_team_imageUrl = game_info['data']['players'][j]['team']['imageUrl']
                game_player_side = game_info['data']['players'][j]['side'].replace("blue", "블루").replace("red", "레드")
                game_player_kills = game_info['data']['players'][j]['kills']
                game_player_deaths = game_info['data']['players'][j]['deaths']
                game_player_assists = game_info['data']['players'][j]['assists']
                try: game_player_kda = ((game_player_kills + game_player_assists) / game_player_deaths).__round__(2)
                except: game_player_kda = "Perfect"
                game_player_championId = game_info['data']['players'][j]['championId']
                game_player_spells = game_info['data']['players'][j]['spells']
                game_player_runes_primary = game_info['data']['players'][j]['runes']['primary']
                game_player_runes_sub = game_info['data']['players'][j]['runes']['sub']
                game_player_items = game_info['data']['players'][j]['items']
                game_player_level = game_info['data']['players'][j]['level']
                game_player_creepScore = game_info['data']['players'][j]['creepScore']
                game_player_goldEarned = game_info['data']['players'][j]['goldEarned']
                game_player_visionWardsBought = game_info['data']['players'][j]['visionWardsBought']
                game_player_totalDamageDealtToChampions = game_info['data']['players'][j]['totalDamageDealtToChampions']
                game_player_totalDamageTaken = game_info['data']['players'][j]['totalDamageTaken']
                game_player_doubleKills = game_info['data']['players'][j]['doubleKills']
                game_player_tripleKills = game_info['data']['players'][j]['tripleKills']
                game_player_quadraKills = game_info['data']['players'][j]['quadraKills']
                game_player_pentaKills = game_info['data']['players'][j]['pentaKills']

                player_templete = {
                    "id": game_player_id,
                    "nickName": game_player_nickName,
                    "position": game_player_position,
                    "nationality": game_player_nationality,
                    "imageUrl": game_player_imageUrl,
                    "team_id": game_player_team_id,
                    "team_name": game_player_team_name,
                    "team_acronym": game_player_team_acronym,
                    "team_nationality": game_player_team_nationality,
                    "team_imageUrl": game_player_team_imageUrl,
                    "side": game_player_side,
                    "kills": game_player_kills,
                    "deaths": game_player_deaths,
                    "assists": game_player_assists,
                    "kda": game_player_kda,
                    "championId": game_player_championId,
                    "spells": game_player_spells,
                    "runes_primary": game_player_runes_primary,
                    "runes_sub": game_player_runes_sub,
                    "items": game_player_items,
                    "level": game_player_level,
                    "creepScore": game_player_creepScore,
                    "goldEarned": game_player_goldEarned,
                    "visionWardsBought": game_player_visionWardsBought,
                    "totalDamageDealtToChampions": game_player_totalDamageDealtToChampions,
                    "totalDamageTaken": game_player_totalDamageTaken,
                    "doubleKills": game_player_doubleKills,
                    "tripleKills": game_player_tripleKills,
                    "quadraKills": game_player_quadraKills,
                    "pentaKills": game_player_pentaKills
                }

                # 플레이어 포지션 순서 정렬(탑, 정글, 미드, 원딜, 서포터 순)
                if game_player_side == "블루":
                    if (game_player_position == "탑") and (player_check_top_blue == False):
                        box_player.append(player_templete)
                        player_check_top_blue = True
                    if (game_player_position == "정글") and (player_check_jun_blue == False) and (player_check_top_blue == True):
                        box_player.append(player_templete)
                        player_check_jun_blue = True
                    if (game_player_position == "미드") and (player_check_mid_blue == False) and (player_check_jun_blue == True):
                        box_player.append(player_templete)
                        player_check_mid_blue = True
                    if (game_player_position == "원딜") and (player_check_adc_blue == False) and (player_check_mid_blue == True):
                        box_player.append(player_templete)
                        player_check_adc_blue = True
                    if (game_player_position == "서포터") and (player_check_sup_blue == False) and (player_check_adc_blue == True):
                        box_player.append(player_templete)
                        player_check_sup_blue = True
                if (game_player_side == "레드") and (player_check_sup_blue == True):
                    if (game_player_position == "탑") and (player_check_top_red == False) and (player_check_sup_blue == True):
                        box_player.append(player_templete)
                        player_check_top_red = True
                    if (game_player_position == "정글") and (player_check_jun_red == False) and (player_check_top_red == True):
                        box_player.append(player_templete)
                        player_check_jun_red = True
                    if (game_player_position == "미드") and (player_check_mid_red == False) and (player_check_jun_red == True):
                        box_player.append(player_templete)
                        player_check_mid_red = True
                    if (game_player_position == "원딜") and (player_check_adc_red == False) and (player_check_mid_red == True):
                        box_player.append(player_templete)
                        player_check_adc_red = True
                    if (game_player_position == "서포터") and (player_check_sup_red == False) and (player_check_adc_red == True):
                        box_player.append(player_templete)
                        player_check_sup_red = True

        box_game_info = {
            "id": game_id,
            "status": game_status,
            "finished": game_finished,
            "beginAt": game_beginAt,
            "endAt": game_endAt,
            "length": game_length,
            "detailedStats": game_detailedStats,
            "winner_id": game_winner_id,
            "winner_name": game_winner_name,
            "winner_acronym": game_winner_acronym,
            "winner_nationality": game_winner_nationality,
            "winner_imageUrl": game_winner_imageUrl,
            "teams": box_team,
            "players": box_player
        }

    else:
        return game_info

    return box_game_info
