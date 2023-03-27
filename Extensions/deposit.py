# -*- coding: utf-8 -*-

# 패키지 라이브러리 설정
import sqlite3
import json
import os

# league.json 파일 불러오기
try:
    with open(r"./league.json", "rt", encoding="UTF8") as leagueJson:
        leagues = json.load(leagueJson)['leagues']
except: print("league.json이 로드되지 않음")


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
