# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import sqlite3
import os

leagues = {
    0: {"id": "85", "name": "League of Legends Circuit Oceania", "shortName": "LCO", "region": "OCE"},
    1: {"id": "86", "name": "Pacific Championship Series", "shortName": "PCS", "region": "SEA"},
    2: {"id": "87", "name": "Liga Latinoamérica", "shortName": "LLA", "region": "LAT"},
    3: {"id": "88", "name": "League of Legends Championship Series", "shortName": "LCS", "region": "NA"},
    4: {"id": "89", "name": "League of Legends European Championship", "shortName": "LEC", "region": "EU"},
    5: {"id": "90", "name": "Vietnam Championship Series", "shortName": "VCS", "region": "VN"},
    6: {"id": "91", "name": "League of Legends Continental League", "shortName": "LCL", "region": "CIS"},
    7: {"id": "92", "name": "League of Legends Japan League", "shortName": "LJL", "region": "JP"},
    8: {"id": "93", "name": "Turkish Championship League", "shortName": "TCL", "region": "TR"},
    9: {"id": "94", "name": "Campeonato Brasileiro de League of Legends", "shortName": "CBLOL", "region": "BR"},
    10: {"id": "95", "name": "Oceanic Pro League", "shortName": "OPL", "region": "COE"},
    11: {"id": "96", "name": "League of Legends World Championship", "shortName": "Worlds", "region": "INT"},
    12: {"id": "97", "name": "League of Legends Master Series", "shortName": "LMS", "region": "LMS"},
    13: {"id": "98", "name": "League of Legends Pro League", "shortName": "LPL", "region": "CN"},
    14: {"id": "99", "name": "League of Legends Champions Korea", "shortName": "LCK", "region": "KR"},
    15: {"id": "100", "name": "Mid-Season Invitational", "shortName": "MSI", "region": "INT"}
}


class DepositPoint:

    def deposit_point(match_data, bet_box):

        if match_data['data']['match_set'] == 1:
            for data_user in os.listdir(r"./Data/User"):    
                match_name = f"{match_data['data']['team_1']} vs {match_data['data']['team_2']}"

                if data_user.endswith(".sqlite"):
                    userID = int(data_user.replace("user_", "").split(".")[0])

                    userDB = sqlite3.connect(rf"./Data/User/{data_user}", isolation_level=None)
                    userCURSOR = userDB.cursor()

                    try:
                        betting_result = userCURSOR.execute(f"SELECT * FROM \"{match_data['data']['match_id']}\"").fetchone()
                        result = userCURSOR.execute(f"SELECT * FROM data WHERE UserID = {userID}").fetchone()
                        userCURSOR.execute(f"DROP TABLE \"{match_data['data']['match_id']}\"")

                        if (betting_result[1] == match_data['data']['match_winner_shortName']):
                            if (betting_result[1] == match_name.split(' vs ')[0]): reward = (bet_box[0] / bet_box[1]).__round__()
                            elif (betting_result[1] == match_name.split(' vs ')[1]): reward = (bet_box[0] / bet_box[2]).__round__()
                            # userCURSOR.execute("UPDATE data SET TotalPoint = ?, Point = ?, CorrectAnswer = ? WHERE UserID = ?", ((result[1] + reward), (result[2] + betting_result[2] + reward), (result[4] + 1), userID))
                            userCURSOR.execute("UPDATE data SET TotalPoint = ?, Point = ?, CorrectAnswer = ? WHERE UserID = ?", ((result[1] + reward), (result[2] + reward), (result[4] + 1), userID))

                        else:
                            userCURSOR.execute("UPDATE data SET WrongAnswer = ? WHERE UserID = ?", ((result[5] + 1), userID))
                    except:
                        pass

                    userDB.close()

            bettingDB = sqlite3.connect(rf"./Data/betting.sqlite", isolation_level=None)
            bettingCURSOR = bettingDB.cursor()

            for i in range(16):
                result = bettingCURSOR.execute(f"SELECT * FROM {leagues[i]['shortName']}").fetchall()
                try: bettingCURSOR.execute(f"DELETE FROM {leagues[i]['shortName']} WHERE ID = '{match_data['data']['match_id']}'")
                except: pass

            bettingDB.close()

        else:
            pass
