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
    game_id = ""
    game_status = ""
    game_finished = False
    game_beginAt = ""
    game_endAt = ""
    game_length = ""
    game_detailedStats = ""
    game_team_id = ""
    game_team_name = ""
    game_team_acronym = ""
    game_team_nationality = ""
    game_team_imageUrl = ""
    game_team_kills = ""
    game_team_deaths = ""
    game_team_assists = ""
    game_team_side = ""
    game_team_towerKills = ""
    game_team_dragonKills = ""
    game_team_elderDragonKills = ""
    game_team_baronKills = ""
    game_team_inhibitorKills = ""
    game_team_heraldKills = ""
    game_team_goldEarned = ""
    game_team_bans = []
    game_player_id = ""
    game_player_nickName = ""
    game_player_position = ""
    game_player_nationality = ""
    game_player_imageUrl = ""
    game_player_kills = ""
    game_player_deaths = ""
    game_player_assists = ""
    game_player_kda = ""
    game_player_championId = ""
    game_player_spells = []
    game_player_runes_primary = []
    game_player_runes_sub = []
    game_player_items = []
    game_player_level = ""
    game_player_creepScore = ""
    game_player_goldEarned = ""
    game_player_visionWardsBought = ""
    game_player_totalDamageDealtToChampions = ""
    game_player_totalDamageTaken = ""
    game_player_doubleKills = False
    game_player_tripleKills = False
    game_player_quadraKills = False
    game_player_pentaKills = False
    game_winner_id = ""
    game_winner_name = ""
    game_winner_acronym = ""
    game_winner_nationality = ""
    game_winner_imageUrl = ""

    game_info = opgg.game_info_by_id(match_id=match_id, match_set=match_set)

    game_id = game_info['data']['id']
    game_status = game_info['data']['status']
    game_finished = game_info['data']['finished']
    game_beginAt = game_info['data']['beginAt']
    game_endAt = game_info['data']['endAt']
    game_length = game_info['data']['length']
    game_detailedStats = game_info['data']['detailedStats']
    for i in range(len(game_info['data']['teams'])):
        game_team_id = game_info['data']['teams'][i]['team']['id']
        game_team_name = game_info['data']['teams'][i]['team']['name']
        game_team_acronym = game_info['data']['teams'][i]['team']['acronym']
        game_team_nationality = game_info['data']['teams'][i]['team']['nationality']
        game_team_imageUrl = game_info['data']['teams'][i]['team']['imageUrl']
        game_team_kills = game_info['data']['teams'][i]['kills']
        game_team_deaths = game_info['data']['teams'][i]['deaths']
        game_team_assists = game_info['data']['teams'][i]['assists']
        game_team_side = game_info['data']['teams'][i]['side']
        game_team_towerKills = game_info['data']['teams'][i]['towerKills']
        game_team_dragonKills = game_info['data']['teams'][i]['dragonKills']
        game_team_elderDragonKills = game_info['data']['teams'][i]['elderDrakeKills']
        game_team_baronKills = game_info['data']['teams'][i]['baronKills']
        game_team_inhibitorKills = game_info['data']['teams'][i]['inhibitorKills']
        game_team_heraldKills = game_info['data']['teams'][i]['heraldKills']
        game_team_goldEarned = game_info['data']['teams'][i]['goldEarned']
        game_team_bans = game_info['data']['teams'][i]['bans']
    for j in range(len(game_info['data']['players'])):
        game_player_id = game_info['data']['players'][j]['player']['id']
        game_player_nickName = game_info['data']['players'][j]['player']['nickName']
        game_player_position = game_info['data']['players'][j]['player']['position'].replace("top", "탑").replace("jun", "정글").replace("mid", "미드").replace("adc", "원딜").replace("sup", "서포터")
        game_player_nationality = game_info['data']['players'][j]['player']['nationality']
        game_player_imageUrl = game_info['data']['players'][j]['player']['imageUrl']
        game_player_kills = game_info['data']['players'][j]['kills']
        game_player_deaths = game_info['data']['players'][j]['deaths']
        game_player_assists = game_info['data']['players'][j]['assists']
        game_player_kda = ((game_player_kills + game_player_assists) / game_player_deaths).__round__(2)
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
    game_winner_id = game_info['data']['winner']['id']
    game_winner_name = game_info['data']['winner']['name']
    game_winner_acronym = game_info['data']['winner']['acronym']
    game_winner_nationality = game_info['data']['winner']['nationality']
    game_winner_imageUrl = game_info['data']['winner']['imageUrl']

    box_game_info = {
        "id": game_id,
        "status": game_status,
        "finished": game_finished,
        "beginAt": game_beginAt,
        "endAt": game_endAt,
        "length": game_length,
        "detailedStats": game_detailedStats,
        "team_id": game_team_id,
        "team_name": game_team_name,
        "team_acronym": game_team_acronym,
        "team_nationalty": game_team_nationality,
        "team_imageUrl": game_team_imageUrl,
        "team_kills": game_team_kills,
        "team_deaths": game_team_deaths,
        "team_assists": game_team_assists,
        "team_side": game_team_side,
        "team_towerKills": game_team_towerKills,
        "team_dragonKills": game_team_dragonKills,
        "team_elderDragonKills": game_team_elderDragonKills,
        "team_baronKills": game_team_baronKills,
        "team_inhibitorKills": game_team_inhibitorKills,
        "team_heraldKills": game_team_heraldKills,
        "team_goldEarned": game_team_goldEarned,
        "team_bans": game_team_bans,
        "player_id": game_player_id,
        "player_nickName": game_player_nickName,
        "player_position": game_player_position,
        "player_nationality": game_player_nationality,
        "player_imageUrl": game_player_imageUrl,
        "player_kills": game_player_kills,
        "player_deaths": game_player_deaths,
        "player_assists": game_player_assists,
        "player_kda": game_player_kda,
        "player_championId": game_player_championId,
        "player_spells": game_player_spells,
        "player_runes_primary": game_player_runes_primary,
        "player_runes_sub": game_player_runes_sub,
        "player_items": game_player_items,
        "player_level": game_player_level,
        "player_creepScore": game_player_creepScore,
        "player_goldEarned": game_player_goldEarned,
        "player_visionWardsBought": game_player_visionWardsBought,
        "player_totalDamageDealtToChampions": game_player_totalDamageDealtToChampions,
        "player_totalDamageTaken": game_player_totalDamageTaken,
        "player_doubleKills": game_player_doubleKills,
        "player_tripleKills": game_player_tripleKills,
        "player_quadraKills": game_player_quadraKills,
        "player_pentaKills": game_player_pentaKills,
        "winner_id": game_winner_id,
        "winner_name": game_winner_name,
        "winner_acronym": game_winner_acronym,
        "winner_nationality": game_winner_nationality,
        "winner_imageUrl": game_winner_imageUrl
    }

    return box_game_info
