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
        match_info = opgg.match_info_by_id(recentMatches[i]['id'])

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
