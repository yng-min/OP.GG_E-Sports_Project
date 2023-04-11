# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
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
    team_discord = ""
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
            team_discord = teams_info['data'][i]['team']['discord']
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
                "discord": team_discord,
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
