import opgg


def get_league_standing(tournamentId):

    box_team = []
    team_id = ""
    team_name = ""
    team_acronym = ""
    team_nationality = ""
    team_foundedAt = ""
    team_imageUrl = ""
    team_youtube = ""
    team_twitter = ""
    team_instagram = ""
    team_facebook = ""
    team_website = ""
    team_position = ""
    team_previously = ""
    team_setWin = ""
    team_setLose = ""
    team_recentMatches = ""

    teams_info = opgg.league_standing(tournamentId=tournamentId[0])

    if teams_info['error'] == False:
        for i in range(len(teams_info['data'])):
            team_id = teams_info['data'][i]['team']['id']
            team_name = teams_info['data'][i]['team']['name']
            team_acronym = teams_info['data'][i]['team']['acronym']
            team_nationality = teams_info['data'][i]['team']['nationality']
            team_foundedAt = teams_info['data'][i]['team']['foundedAt']
            team_imageUrl = teams_info['data'][i]['team']['imageUrl']
            team_youtube = teams_info['data'][i]['team']['youtube']
            team_twitter = teams_info['data'][i]['team']['twitter']
            team_instagram = teams_info['data'][i]['team']['instagram']
            team_facebook = teams_info['data'][i]['team']['facebook']
            team_website = teams_info['data'][i]['team']['website']
            team_position = teams_info['data'][i]['position']
            team_previously = teams_info['data'][i]['previously']
            team_point = teams_info['data'][i]['point']
            team_win = teams_info['data'][i]['win']
            team_lose = teams_info['data'][i]['lose']
            team_setWin = teams_info['data'][i]['setWin']
            team_setLose = teams_info['data'][i]['setLose']
            team_recentMatches = teams_info['data'][i]['recentMatches']

            box_team.append({
                "id": team_id,
                "name": team_name,
                "acronym": team_acronym,
                "nationality": team_nationality,
                "foundedAt": team_foundedAt,
                "imageUrl": team_imageUrl,
                "youtube": team_youtube,
                "twitter": team_twitter,
                "instagram": team_instagram,
                "facebook": team_facebook,
                "website": team_website,
                "position": team_position,
                "previously": team_previously,
                "point": team_point,
                "win": team_win,
                "lose": team_lose,
                "setWin": team_setWin,
                "setLose": team_setLose,
                "recentMatches": team_recentMatches
            })

    else:
        return teams_info

    return box_team


def get_team_info(tournamentId, teams_id):

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
    players_info = opgg.player_info_by_team(tournamentId[0], teams_id)

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


def get_player_mvp_rank(tournamentId):

    box_players = []

    if tournamentId == None: return None
    players_info = opgg.player_mvp_rank(tournamentId=tournamentId[0])

    if players_info['error'] == False:
        for i in range(len(players_info['data']['mvps'])):
            mvp_player_id = players_info['data']['mvps'][i]['player']['id']
            mvp_player_nickName = players_info['data']['mvps'][i]['player']['nickName']
            mvp_player_nationality = players_info['data']['mvps'][i]['player']['nationality']
            mvp_player_image = players_info['data']['mvps'][i]['player']['imageUrl']
            mvp_player_position = (players_info['data']['mvps'][i]['position']).replace("top", "탑").replace("jun", "정글").replace("mid", "미드").replace("adc", "원딜").replace("sup", "서포터")
            mvp_player_currently = players_info['data']['mvps'][i]['currently']
            mvp_player_previously = players_info['data']['mvps'][i]['previously']
            mvp_player_mvpPoint = players_info['data']['mvps'][i]['mvpPoint']
            mvp_player_games = players_info['data']['mvps'][i]['games']
            mvp_player_kda = (players_info['data']['mvps'][i]['kda']).__round__(2)
            mvp_player_kills = (players_info['data']['mvps'][i]['kills']).__round__(2)
            mvp_player_deaths = (players_info['data']['mvps'][i]['deaths']).__round__(2)
            mvp_player_assists = (players_info['data']['mvps'][i]['assists']).__round__(2)
            mvp_team_id = players_info['data']['mvps'][i]['team']['id']
            mvp_team_name = players_info['data']['mvps'][i]['team']['name']
            mvp_team_acronym = players_info['data']['mvps'][i]['team']['acronym']
            mvp_tournament_id = players_info['data']['mvps'][i]['tournamentId']

            box_players.append({
                "id": mvp_player_id,
                "nickName": mvp_player_nickName,
                "nationality": mvp_player_nationality,
                "imageUrl": mvp_player_image,
                "position": mvp_player_position,
                "currently": mvp_player_currently,
                "previously": mvp_player_previously,
                "mvpPoint": mvp_player_mvpPoint,
                "games": mvp_player_games,
                "kda": mvp_player_kda,
                "kills": mvp_player_kills,
                "deaths": mvp_player_deaths,
                "assists": mvp_player_assists,
                "team_id": mvp_team_id,
                "team_name": mvp_team_name,
                "team_acronym": mvp_team_acronym,
                "tournamentId": mvp_tournament_id
            })

    else:
        return players_info

    return box_players
