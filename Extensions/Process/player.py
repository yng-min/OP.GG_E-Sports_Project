# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import opgg


def get_player_info_by_id(playerId):

    box_player = []
    player_id = ""
    player_nickName = ""
    player_firstName = ""
    player_lastName = ""
    player_position = ""
    player_natinality = ""
    player_imageUrl = ""
    player_birthday = ""
    player_stream = ""
    player_youtube = ""
    player_twitter = ""
    player_instagram = ""
    player_facebook = ""
    player_discord = ""
    player_team_id = ""
    player_team_name = ""
    player_team_acronym = ""
    player_team_nationality = ""
    player_team_imageUrl = ""

    if playerId == None: return None
    player_info = opgg.player_info_by_id(playerId)

    if player_info['error'] == False:
        for i in range(len(player_info['data'])):
            player_id = player_info['data'][i]['id']
            player_nickName = player_info['data'][i]['nickName']
            player_firstName = player_info['data'][i]['firstName']
            player_lastName = player_info['data'][i]['lastName']
            player_position = player_info['data'][i]['position']
            player_natinality = player_info['data'][i]['nationality']
            player_imageUrl = player_info['data'][i]['imageUrl']
            player_birthday = player_info['data'][i]['birthday']
            player_stream = player_info['data'][i]['stream']
            player_youtube = player_info['data'][i]['youtube']
            player_twitter = player_info['data'][i]['twitter']
            player_instagram = player_info['data'][i]['instagram']
            player_facebook = player_info['data'][i]['facebook']
            player_discord = player_info['data'][i]['discord']
            player_team_id = player_info['data'][i]['currentTeam']['id']
            player_team_name = player_info['data'][i]['currentTeam']['name']
            player_team_acronym = player_info['data'][i]['currentTeam']['acronym']
            player_team_nationality = player_info['data'][i]['currentTeam']['nationality']
            player_team_imageUrl = player_info['data'][i]['currentTeam']['imageUrl']

            box_player.append({
                "id": player_id,
                "nickName": player_nickName,
                "firstName": player_firstName,
                "lastName": player_lastName,
                "position": player_position,
                "nationality": player_natinality,
                "imageUrl": player_imageUrl,
                "birthday": player_birthday,
                "stream": player_stream,
                "youtube": player_youtube,
                "twitter": player_twitter,
                "instagram": player_instagram,
                "facebook": player_facebook,
                "discord": player_discord,
                "team_id": player_team_id,
                "team_name": player_team_name,
                "team_acronym": player_team_acronym,
                "team_nationality": player_team_nationality,
                "team_imageUrl": player_team_imageUrl
            })

    else:
        return box_player
        
    return box_player


def get_player_info_by_nickname(playerNickname):

    box_player = []
    player_id = ""
    player_nickName = ""
    player_firstName = ""
    player_lastName = ""
    player_position = ""
    player_natinality = ""
    player_imageUrl = ""
    player_birthday = ""
    player_stream = ""
    player_youtube = ""
    player_twitter = ""
    player_instagram = ""
    player_facebook = ""
    player_discord = ""
    player_team_id = ""
    player_team_name = ""
    player_team_acronym = ""
    player_team_nationality = ""
    player_team_imageUrl = ""

    if playerNickname == None: return None
    player_info = opgg.player_info_by_nickname(playerNickname)

    if player_info['error'] == False:
        player_id = player_info['data']['id']
        player_nickName = player_info['data']['nickName']
        player_firstName = player_info['data']['firstName']
        player_lastName = player_info['data']['lastName']
        player_position = player_info['data']['position']
        player_natinality = player_info['data']['nationality']
        player_imageUrl = player_info['data']['imageUrl']
        player_birthday = player_info['data']['birthday']
        player_stream = player_info['data']['stream']
        player_youtube = player_info['data']['youtube']
        player_twitter = player_info['data']['twitter']
        player_instagram = player_info['data']['instagram']
        player_facebook = player_info['data']['facebook']
        player_discord = player_info['data']['discord']
        player_team_id = player_info['data']['currentTeam']['id']
        player_team_name = player_info['data']['currentTeam']['name']
        player_team_acronym = player_info['data']['currentTeam']['acronym']
        player_team_nationality = player_info['data']['currentTeam']['nationality']
        player_team_imageUrl = player_info['data']['currentTeam']['imageUrl']

        box_player.append({
            "id": player_id,
            "nickName": player_nickName,
            "firstName": player_firstName,
            "lastName": player_lastName,
            "position": player_position,
            "nationality": player_natinality,
            "imageUrl": player_imageUrl,
            "birthday": player_birthday,
            "stream": player_stream,
            "youtube": player_youtube,
            "twitter": player_twitter,
            "instagram": player_instagram,
            "facebook": player_facebook,
            "discord": player_discord,
            "team_id": player_team_id,
            "team_name": player_team_name,
            "team_acronym": player_team_acronym,
            "team_nationality": player_team_nationality,
            "team_imageUrl": player_team_imageUrl
        })

    else:
        return box_player
        
    return box_player


def get_team_info_by_id(tournamentId, teamId):

    box_player = []
    player_templete = {}
    player_check_top = False
    player_check_jun = False
    player_check_mid = False
    player_check_adc = False
    player_check_sup = False
    player_id = ""
    player_nickName = ""
    player_firstName = ""
    player_lastName = ""
    player_position = ""
    player_nationality = ""
    player_imageUrl = ""
    player_birthday = ""
    player_stream = ""
    player_youtube = ""
    player_twitter = ""
    player_instagram = ""
    player_facebook = ""
    player_discord = ""
    player_team_id = ""
    player_team_name = ""
    player_team_acronym = ""
    player_team_nationality = ""
    player_team_imageUrl = ""
    player_stat_games = ""
    player_stat_winRate = ""
    player_stat_wins = ""
    player_stat_loses = ""
    player_stat_kills = ""
    player_stat_deaths = ""
    player_stat_assists = ""
    player_stat_kda = ""
    player_stat_dpm = ""
    player_stat_dtpm = ""
    player_stat_gpm = ""
    player_stat_cspm = ""
    player_stat_dpgr = ""
    player_stat_firstBlood = ""
    player_stat_firstTower = ""
    player_stat_wardsPlaced = ""
    player_stat_wardsKilled = ""

    if tournamentId == None: return None
    players_info = opgg.players_info_by_team(tournamentId[0], teamId)

    if players_info['error'] == False:
        for i in range(len(players_info['data'])):
            for j in range(len(players_info['data'])):
                player_id = players_info['data'][j]['player']['id']
                player_nickName = players_info['data'][j]['player']['nickName']
                player_firstName = players_info['data'][j]['player']['firstName']
                player_lastName = players_info['data'][j]['player']['lastName']
                player_position = players_info['data'][j]['player']['position'].replace("top", "탑").replace("jun", "정글").replace("mid", "미드").replace("adc", "원딜").replace("sup", "서포터")
                player_nationality = players_info['data'][j]['player']['nationality']
                player_imageUrl = players_info['data'][j]['player']['imageUrl']
                player_birthday = players_info['data'][j]['player']['birthday']
                player_stream = players_info['data'][j]['player']['stream']
                player_youtube = players_info['data'][j]['player']['youtube']
                player_twitter = players_info['data'][j]['player']['twitter']
                player_instagram = players_info['data'][j]['player']['instagram']
                player_facebook = players_info['data'][j]['player']['facebook']
                player_discord = players_info['data'][j]['player']['discord']
                player_team_id = players_info['data'][j]['playerStat']['team']['id']
                player_team_name = players_info['data'][j]['playerStat']['team']['name']
                player_team_acronym = players_info['data'][j]['playerStat']['team']['acronym']
                player_team_nationality = players_info['data'][j]['playerStat']['team']['acronym']
                player_team_imageUrl = players_info['data'][j]['playerStat']['team']['imageUrl']
                player_stat_games = players_info['data'][j]['playerStat']['games']
                player_stat_winRate = (players_info['data'][j]['playerStat']['winRate'] * 100).__round__(2)
                player_stat_wins = players_info['data'][j]['playerStat']['wins']
                player_stat_loses = players_info['data'][j]['playerStat']['loses']
                player_stat_kills = players_info['data'][j]['playerStat']['kills'].__round__(2)
                player_stat_deaths = players_info['data'][j]['playerStat']['deaths'].__round__(2)
                player_stat_assists = players_info['data'][j]['playerStat']['assists'].__round__(2)
                player_stat_kda = players_info['data'][j]['playerStat']['kda'].__round__(2)
                player_stat_dpm = players_info['data'][j]['playerStat']['dpm'].__round__(2)
                player_stat_dtpm = players_info['data'][j]['playerStat']['dtpm'].__round__(2)
                player_stat_gpm = players_info['data'][j]['playerStat']['gpm'].__round__(2)
                player_stat_cspm = players_info['data'][j]['playerStat']['cspm'].__round__(2)
                player_stat_dpgr = players_info['data'][j]['playerStat']['dpgr'].__round__(2)
                player_stat_firstBlood = (players_info['data'][j]['playerStat']['firstBlood'] * 100).__round__(2)
                player_stat_firstTower = (players_info['data'][j]['playerStat']['firstTower'] * 100).__round__(2)
                player_stat_wardsPlaced = players_info['data'][j]['playerStat']['wardsPlaced'].__round__(2)
                player_stat_wardsKilled = players_info['data'][j]['playerStat']['wardsKilled'].__round__(2)

                player_templete = {
                    "id": player_id,
                    "nickName": player_nickName,
                    "firstName": player_firstName,
                    "lastName": player_lastName,
                    "position": player_position,
                    "nationality": player_nationality,
                    "imageUrl": player_imageUrl,
                    "birthday": player_birthday,
                    "stream": player_stream,
                    "youtube": player_youtube,
                    "twitter": player_twitter,
                    "instagram": player_instagram,
                    "facebook": player_facebook,
                    "discord": player_discord,
                    "team_id": player_team_id,
                    "team_name": player_team_name,
                    "team_acronym": player_team_acronym,
                    "team_nationality": player_team_nationality,
                    "team_imageUrl": player_team_imageUrl,
                    "stat_games": player_stat_games,
                    "stat_winRate": player_stat_winRate,
                    "stat_wins": player_stat_wins,
                    "stat_loses": player_stat_loses,
                    "stat_kills": player_stat_kills,
                    "stat_deaths": player_stat_deaths,
                    "stat_assists": player_stat_assists,
                    "stat_kda": player_stat_kda,
                    "stat_dpm": player_stat_dpm,
                    "stat_dtpm": player_stat_dtpm,
                    "stat_gpm": player_stat_gpm,
                    "stat_cspm": player_stat_cspm,
                    "stat_dpgr": player_stat_dpgr,
                    "stat_firstBlood": player_stat_firstBlood,
                    "stat_firstTower": player_stat_firstTower,
                    "stat_wardsPlaced": player_stat_wardsPlaced,
                    "stat_wardsKilled": player_stat_wardsKilled
                }

                # 플레이어 포지션 순서 정렬(탑, 정글, 미드, 원딜, 서포터 순)
                if (player_check_top == False) and (player_position == "탑"):
                    box_player.append(player_templete)
                    player_check_top = True
                if (player_check_top == True) and (player_check_jun == False) and (player_position == "정글"):
                    box_player.append(player_templete)
                    player_check_jun = True
                if (player_check_top == True) and (player_check_jun == True) and (player_check_mid == False) and (player_position == "미드"):
                    box_player.append(player_templete)
                    player_check_mid = True
                if (player_check_top == True) and (player_check_jun == True) and (player_check_mid == True) and (player_check_adc == False) and (player_position == "원딜"):
                    box_player.append(player_templete)
                    player_check_adc = True
                if (player_check_top == True) and (player_check_jun == True) and (player_check_mid == True) and (player_check_adc == True) and (player_check_sup == False) and (player_position == "서포터"):
                    box_player.append(player_templete)
                    player_check_sup = True

    else:
        return players_info

    return box_player
