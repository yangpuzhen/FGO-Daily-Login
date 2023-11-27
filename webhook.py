import main
import requests
import user


def topLogin(data: list) -> None:
    endpoint = main.webhook_discord_url

    rewards: user.Rewards = data[0]
    login: user.Login = data[1]
    bonus: user.Bonus or str = data[2]

    messageBonus = ''
    nl = '\n'

    if bonus != "No Bonus":
        messageBonus += f"__{bonus.message}__{nl}```{nl.join(bonus.items)}```"

        if bonus.bonus_name != None:
            messageBonus += f"{nl}__{bonus.bonus_name}__{nl}{bonus.bonus_detail}{nl}```{nl.join(bonus.bonus_camp_items)}```"

        messageBonus += "\n"

    jsonData = {
        "content": None,
        "embeds": [
            {
                "title": "FGO每日登录 - " + main.fate_region,
                "description": f"按计划进行的FGO每日登录 \n\n{messageBonus}",
                "color": 563455,
                "fields": [
                    {
                        "name": "等级",
                        "value": f"{rewards.level}",
                        "inline": True
                    },
                    {
                        "name": "呼符",
                        "value": f"{rewards.ticket}",
                        "inline": True
                    },
                    {
                        "name": "圣晶石",
                        "value": f"{rewards.stone}",
                        "inline": True
                    },
                    {
                        "name": "登录天数",
                        "value": f"{login.login_days}",
                        "inline": True
                    },
                    {
                        "name": "总登录天数",
                        "value": f"{login.total_days}",
                        "inline": True
                    },
                    {
                        "name": "友情点",
                        "value": f"{login.total_fp}",
                        "inline": True
                    },
                    {
                        "name": "好友分值",
                        "value": f"+{login.add_fp}",
                        "inline": True
                    },
                    {
                        "name": "体力上限",
                        "value": f"{login.act_max}",
                        "inline": True
                    }
                ],
                "thumbnail": {
                    "url": "https://grandorder.wiki/images/thumb/3/3d/Icon_Item_Saint_Quartz.png/200px-Icon_Item_Saint_Quartz.png"
                }
            }
        ],
        "attachments": []
    }

    headers = {
        "Content-Type": "application/json"
    }

    requests.post(endpoint, json=jsonData, headers=headers)


def drawFP(servants, missions) -> None:
    endpoint = main.webhook_discord_url

    message_mission = ""
    message_servant = ""

    if (len(servants) > 0):
        servants_atlas = requests.get(
            f"https://api.atlasacademy.io/export/JP/basic_svt_lang_en.json").json()

        svt_dict = {svt["id"]: svt for svt in servants_atlas}

        for servant in servants:
            svt = svt_dict[servant.objectId]
            message_servant += f"`{svt['originalName']}` "

    if(len(missions) > 0):
        for mission in missions:
            message_mission += f"__{mission.message}__\n{mission.progressTo}/{mission.condition}\n"

    jsonData = {
        "content": None,
        "embeds": [
            {
                "title": "FGO每日登录 - " + main.fate_region,
                "description": f"按计划进行的FGO每日登录.\n\n{message_mission}",
                "color": 5750876,
                "fields": [
                    {
                        "name": "友情池抽取结果",
                        "value": f"{message_servant}",
                        "inline": False
                    }
                ],
                "thumbnail": {
                    "url": "https://i.imgur.com/LJMPpP8.png"
                }
            }
        ],
        "attachments": []
    }

    headers = {
        "Content-Type": "application/json"
    }

    requests.post(endpoint, json=jsonData, headers=headers)
