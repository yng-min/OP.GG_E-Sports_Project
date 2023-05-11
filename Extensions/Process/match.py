# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import opgg


def get_match_info_by_id(matchId: str):

    box_match_info = {}
    match_id = ""
    match_name = ""
    match_originalScheduledAt = ""
    match_scheduledAt = ""
    match_beginAt = ""
    match_endAt = ""
    match_status = ""
    match_numberOfGames = 0
    match_liveSupported = False
    match_liveOpensAt = ""
    match_streams_isMain = False
    match_streams_isOfficial = False
    match_streams_rawUrl = ""
    match_homeTeam_id = ""
    match_homeTeam_name = ""
    match_homeTeam_acronym = ""
    match_homeTeam_nationality = ""
    match_homeTeam_foundedAt = ""
    match_homeTeam_imageUrl = ""
    match_homeTeam_youtube = ""
    match_homeTeam_twitter = ""
    match_homeTeam_instagram = ""
    match_homeTeam_facebook = ""
    match_homeTeam_discord = ""
    match_homeTeam_website = ""
    match_awayTeam_id = ""
    match_awayTeam_name = ""
    match_awayTeam_acronym = ""
    match_awayTeam_nationality = ""
    match_awayTeam_foundedAt = ""
    match_awayTeam_imageUrl = ""
    match_awayTeam_youtube = ""
    match_awayTeam_twitter = ""
    match_awayTeam_instagram = ""
    match_awayTeam_facebook = ""
    match_awayTeam_discord = ""
    match_awayTeam_website = ""
    match_homeTeamRank_position = 0
    match_homeTeamRank_previously = 0
    match_homeTeamRank_point = 0
    match_homeTeamRank_setWin = 0
    match_homeTeamRank_setLose = 0
    match_homeTeamRank_win = 0
    match_homeTeamRank_lose = 0
    match_awayTeamRank_position = 0
    match_awayTeamRank_previously = 0
    match_awayTeamRank_point = 0
    match_awayTeamRank_setWin = 0
    match_awayTeamRank_setLose = 0
    match_awayTeamRank_win = 0
    match_awayTeamRank_lose = 0

    match_info = opgg.match_info_by_id(matchId=matchId)

    if match_info['error'] == False:
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
        match_streams_isMain = match_info['data'][0]['streams'][0]['isMain']
        match_streams_isOfficial = match_info['data'][0]['streams'][0]['isOfficial']
        match_streams_rawUrl = match_info['data'][0]['streams'][0]['rawUrl']
        match_homeTeam_id = match_info['data'][0]['homeTeam']['id']
        match_homeTeam_name = match_info['data'][0]['homeTeam']['name']
        match_homeTeam_acronym = match_info['data'][0]['homeTeam']['acronym']
        match_homeTeam_nationality = match_info['data'][0]['homeTeam']['nationality']
        match_homeTeam_foundedAt = match_info['data'][0]['homeTeam']['foundedAt']
        match_homeTeam_imageUrl = match_info['data'][0]['homeTeam']['imageUrl']
        match_homeTeam_youtube = match_info['data'][0]['homeTeam']['youtube']
        match_homeTeam_twitter = match_info['data'][0]['homeTeam']['twitter']
        match_homeTeam_instagram = match_info['data'][0]['homeTeam']['instagram']
        match_homeTeam_facebook = match_info['data'][0]['homeTeam']['facebook']
        match_homeTeam_discord = match_info['data'][0]['homeTeam']['discord']
        match_homeTeam_website = match_info['data'][0]['homeTeam']['website']
        match_awayTeam_id = match_info['data'][0]['awayTeam']['id']
        match_awayTeam_name = match_info['data'][0]['awayTeam']['name']
        match_awayTeam_acronym = match_info['data'][0]['awayTeam']['acronym']
        match_awayTeam_nationality = match_info['data'][0]['awayTeam']['nationality']
        match_awayTeam_foundedAt = match_info['data'][0]['awayTeam']['foundedAt']
        match_awayTeam_imageUrl = match_info['data'][0]['awayTeam']['imageUrl']
        match_awayTeam_youtube = match_info['data'][0]['awayTeam']['youtube']
        match_awayTeam_twitter = match_info['data'][0]['awayTeam']['twitter']
        match_awayTeam_instagram = match_info['data'][0]['awayTeam']['instagram']
        match_awayTeam_facebook = match_info['data'][0]['awayTeam']['facebook']
        match_awayTeam_discord = match_info['data'][0]['awayTeam']['discord']
        match_awayTeam_website = match_info['data'][0]['awayTeam']['website']
        match_homeTeamRank_position = match_info['data'][0]['ranks']['homeTeamRank']['position']
        match_homeTeamRank_previously = match_info['data'][0]['ranks']['homeTeamRank']['previously']
        match_homeTeamRank_point = match_info['data'][0]['ranks']['homeTeamRank']['point']
        match_homeTeamRank_setWin = match_info['data'][0]['ranks']['homeTeamRank']['setWin']
        match_homeTeamRank_setLose = match_info['data'][0]['ranks']['homeTeamRank']['setLose']
        match_homeTeamRank_win = match_info['data'][0]['ranks']['homeTeamRank']['win']
        match_homeTeamRank_lose = match_info['data'][0]['ranks']['homeTeamRank']['lose']
        match_awayTeamRank_position = match_info['data'][0]['ranks']['awayTeamRank']['position']
        match_awayTeamRank_previously = match_info['data'][0]['ranks']['awayTeamRank']['previously']
        match_awayTeamRank_point = match_info['data'][0]['ranks']['awayTeamRank']['point']
        match_awayTeamRank_setWin = match_info['data'][0]['ranks']['awayTeamRank']['setWin']
        match_awayTeamRank_setLose = match_info['data'][0]['ranks']['awayTeamRank']['setLose']
        match_awayTeamRank_win = match_info['data'][0]['ranks']['awayTeamRank']['win']
        match_awayTeamRank_lose = match_info['data'][0]['ranks']['awayTeamRank']['lose']

        box_match_info = {
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
            "streams": {
                "isMain": match_streams_isMain,
                "isOfficial": match_streams_isOfficial,
                "rawUrl": match_streams_rawUrl
            },
            "homeTeam": {
                "id": match_homeTeam_id,
                "name": match_homeTeam_name,
                "acronym": match_homeTeam_acronym,
                "nationality": match_homeTeam_nationality,
                "foundedAt": match_homeTeam_foundedAt,
                "imageUrl": match_homeTeam_imageUrl,
                "youtube": match_homeTeam_youtube,
                "twitter": match_homeTeam_twitter,
                "instagram": match_homeTeam_instagram,
                "facebook": match_homeTeam_facebook,
                "discord": match_homeTeam_discord,
                "website": match_homeTeam_website,
                "rank": {
                    "position": match_homeTeamRank_position,
                    "previously": match_homeTeamRank_previously,
                    "point": match_homeTeamRank_point,
                    "setWin": match_homeTeamRank_setWin,
                    "setLose": match_homeTeamRank_setLose,
                    "win": match_homeTeamRank_win,
                    "lose": match_homeTeamRank_lose
                }
            },
            "awayTeam": {
                "id": match_awayTeam_id,
                "name": match_awayTeam_name,
                "acronym": match_awayTeam_acronym,
                "nationality": match_awayTeam_nationality,
                "foundedAt": match_awayTeam_foundedAt,
                "imageUrl": match_awayTeam_imageUrl,
                "youtube": match_awayTeam_youtube,
                "twitter": match_awayTeam_twitter,
                "instagram": match_awayTeam_instagram,
                "facebook": match_awayTeam_facebook,
                "discord": match_awayTeam_discord,
                "website": match_awayTeam_website,
                "rank": {
                    "position": match_awayTeamRank_position,
                    "previously": match_awayTeamRank_previously,
                    "point": match_awayTeamRank_point,
                    "setWin": match_awayTeamRank_setWin,
                    "setLose": match_awayTeamRank_setLose,
                    "win": match_awayTeamRank_win,
                    "lose": match_awayTeamRank_lose
                }
            }
        }

    else:
        return match_info

    return box_match_info


def get_game_info_by_id(matchId: str, matchSet: str):

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

    game_info = opgg.game_info_by_id(matchId=matchId, matchSet=matchSet)

    if game_info['error'] == False:
        try: game_id = game_info['data']['id']
        except: pass
        try: game_status = game_info['data']['status']
        except: pass
        try: game_finished = game_info['data']['finished']
        except: pass
        try: game_beginAt = game_info['data']['beginAt']
        except: pass
        try: game_endAt = game_info['data']['endAt']
        except: pass
        try: game_length = game_info['data']['length']
        except: pass
        try: game_detailedStats = game_info['data']['detailedStats']
        except: pass

        try: game_winner_id = game_info['data']['winner']['id']
        except: pass
        try: game_winner_name = game_info['data']['winner']['name']
        except: pass
        try: game_winner_acronym = game_info['data']['winner']['acronym']
        except: pass
        try: game_winner_nationality = game_info['data']['winner']['nationality']
        except: pass
        try: game_winner_imageUrl = game_info['data']['winner']['imageUrl']
        except: pass

        for z in range(len(game_info['data']['teams'])):
            for i in range(len(game_info['data']['teams'])):
                try: game_team_id = game_info['data']['teams'][i]['team']['id']
                except: pass
                try: game_team_name = game_info['data']['teams'][i]['team']['name']
                except: pass
                try: game_team_acronym = game_info['data']['teams'][i]['team']['acronym']
                except: pass
                try: game_team_nationality = game_info['data']['teams'][i]['team']['nationality']
                except: pass
                try: game_team_imageUrl = game_info['data']['teams'][i]['team']['imageUrl']
                except: pass
                try: game_team_kills = game_info['data']['teams'][i]['kills']
                except: pass
                try: game_team_deaths = game_info['data']['teams'][i]['deaths']
                except: pass
                try: game_team_assists = game_info['data']['teams'][i]['assists']
                except: pass
                try: game_team_side = game_info['data']['teams'][i]['side'].replace("blue", "블루").replace("red", "레드")
                except: pass
                try: game_team_towerKills = game_info['data']['teams'][i]['towerKills']
                except: pass
                try: game_team_dragonKills = game_info['data']['teams'][i]['dragonKills']
                except: pass
                try: game_team_elderDrakeKills = game_info['data']['teams'][i]['elderDrakeKills']
                except: pass
                try: game_team_baronKills = game_info['data']['teams'][i]['baronKills']
                except: pass
                try: game_team_inhibitorKills = game_info['data']['teams'][i]['inhibitorKills']
                except: pass
                try: game_team_heraldKills = game_info['data']['teams'][i]['heraldKills']
                except: pass
                try: game_team_goldEarned = game_info['data']['teams'][i]['goldEarned']
                except: pass
                try: game_team_bans = game_info['data']['teams'][i]['bans']
                except: pass

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
                try: game_player_id = game_info['data']['players'][j]['player']['id']
                except: pass
                try: game_player_nickName = game_info['data']['players'][j]['player']['nickName']
                except: pass
                try: game_player_position = game_info['data']['players'][j]['player']['position'].replace("top", "탑").replace("jun", "정글").replace("mid", "미드").replace("adc", "원딜").replace("sup", "서포터")
                except: pass
                try: game_player_nationality = game_info['data']['players'][j]['player']['nationality']
                except: pass
                try: game_player_imageUrl = game_info['data']['players'][j]['player']['imageUrl']
                except: pass
                try: game_player_team_id = game_info['data']['players'][j]['team']['id']
                except: pass
                try: game_player_team_name = game_info['data']['players'][j]['team']['name']
                except: pass
                try: game_player_team_acronym = game_info['data']['players'][j]['team']['acronym']
                except: pass
                try: game_player_team_nationality = game_info['data']['players'][j]['team']['nationality']
                except: pass
                try: game_player_team_imageUrl = game_info['data']['players'][j]['team']['imageUrl']
                except: pass
                try: game_player_side = game_info['data']['players'][j]['side'].replace("blue", "블루").replace("red", "레드")
                except: pass
                try: game_player_kills = game_info['data']['players'][j]['kills']
                except: pass
                try: game_player_deaths = game_info['data']['players'][j]['deaths']
                except: pass
                try: game_player_assists = game_info['data']['players'][j]['assists']
                except: pass

                try: game_player_kda = ((game_player_kills + game_player_assists) / game_player_deaths).__round__(2)
                except: game_player_kda = "Perfect"

                try: game_player_championId = game_info['data']['players'][j]['championId']
                except: pass
                try: game_player_spells = game_info['data']['players'][j]['spells']
                except: pass
                try: game_player_runes_primary = game_info['data']['players'][j]['runes']['primary']
                except: pass
                try: game_player_runes_sub = game_info['data']['players'][j]['runes']['sub']
                except: pass
                try: game_player_items = game_info['data']['players'][j]['items']
                except: pass
                try: game_player_level = game_info['data']['players'][j]['level']
                except: pass
                try: game_player_creepScore = game_info['data']['players'][j]['creepScore']
                except: pass
                try: game_player_goldEarned = game_info['data']['players'][j]['goldEarned']
                except: pass
                try: game_player_visionWardsBought = game_info['data']['players'][j]['visionWardsBought']
                except: pass
                try: game_player_totalDamageDealtToChampions = game_info['data']['players'][j]['totalDamageDealtToChampions']
                except: pass
                try: game_player_totalDamageTaken = game_info['data']['players'][j]['totalDamageTaken']
                except: pass
                try: game_player_doubleKills = game_info['data']['players'][j]['doubleKills']
                except: pass
                try: game_player_tripleKills = game_info['data']['players'][j]['tripleKills']
                except: pass
                try: game_player_quadraKills = game_info['data']['players'][j]['quadraKills']
                except: pass
                try: game_player_pentaKills = game_info['data']['players'][j]['pentaKills']
                except: pass

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


def get_recentMatches(recentMatches: list):

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
        match_info = opgg.match_info_by_id(matchId=recentMatches[i]['id'])

        try: match_id = match_info['data'][0]['id']
        except: pass
        try: match_name = match_info['data'][0]['name']
        except: pass
        try: match_originalScheduledAt = match_info['data'][0]['originalScheduledAt']
        except: pass
        try: match_scheduledAt = match_info['data'][0]['scheduledAt']
        except: pass
        try: match_beginAt = match_info['data'][0]['beginAt']
        except: pass
        try: match_endAt = match_info['data'][0]['endAt']
        except: pass
        try: match_status = match_info['data'][0]['status']
        except: pass
        try: match_numberOfGames = match_info['data'][0]['numberOfGames']
        except: pass
        try: match_liveSupported = match_info['data'][0]['liveSupported']
        except: pass
        try: match_liveOpensAt = match_info['data'][0]['liveOpensAt']
        except: pass
        try: match_streams = match_info['data'][0]['streams']
        except: pass
        try: match_winnerTeam = match_info['data'][0]['winnerTeam']
        except: pass
        try: match_homeTeam = match_info['data'][0]['homeTeam']
        except: pass
        try: match_homeScore = match_info['data'][0]['homeScore']
        except: pass
        try: match_awayTeam = match_info['data'][0]['awayTeam']
        except: pass
        try: match_awayScore = match_info['data'][0]['awayScore']
        except: pass
        try: match_ranks = match_info['data'][0]['ranks']
        except: pass

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
