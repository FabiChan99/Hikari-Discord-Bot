import aiohttp
from discord import Client, InvalidArgument
from discord.ext.commands import Bot
from typing import Union

defaultApplications = {
    'youtube': '755600276941176913',
    'poker': '755827207812677713',
    'betrayal': '773336526917861400',
    'fishing': '814288819477020702',
    'chess': '832012586023256104',
    'music': '880218394199220334'
}


class DiscordTogether():
    def __init__(self, client: Union[Client, Bot]):
        self.client = client

    async def create_link(self, voiceChannelID, option):

        if option and (str(option).lower().replace(" ", "") in defaultApplications.keys()):
            async with aiohttp.ClientSession() as session:
                async with session.post(f"https://discord.com/api/v8/channels/{voiceChannelID}/invites",
                                        json={
                                            'max_age': 86400,
                                            'max_uses': 0,
                                            'target_application_id': defaultApplications[option],
                                            'target_type': 2,
                                            'temporary': False,
                                            'validate': None
                                        },
                                        headers={
                                            'Authorization': f'Bot {self.client.http.token}',
                                            'Content-Type': 'application/json'
                                        }
                                        ) as resp:
                    result = await resp.json()
            if ("errors" in result.keys()) or ("code" not in result.keys()):
                raise ConnectionError("An error occured while retrieving data from Discord API.")
            else:
                return f"https://discord.com/invite/{result['code']}"

        elif option and (str(option).lower().replace("", " ") not in defaultApplications.keys()):
            async with aiohttp.ClientSession() as session:
                async with session.post(f"https://discord.com/api/v8/channels/{voiceChannelID}/invites",
                                        json={
                                            'max_age': 86400,
                                            'max_uses': 0,
                                            'target_application_id': str(option),
                                            'target_type': 2,
                                            'temporary': False,
                                            'validate': None
                                        },
                                        headers={
                                            'Authorization': f'Bot {self.client.http.token}',
                                            'Content-Type': 'application/json'
                                        }
                                        ) as resp:
                    result = await resp.json()
            if ("errors" in result.keys()) or ("code" not in result.keys()):
                if "target_application_id" in result['errors'].keys():
                    raise InvalidArgument(f"\"{str(option)}\" is an invalid custom application ID.")
                else:
                    raise ConnectionError("An error occured while retrieving data from Discord API.")
            else:
                return f"https://discord.com/invite/{result['code']}"
        else:
            raise InvalidArgument(
                "Invalid activity option chosen. You may only choose between (\"youtube\",\"poker\",\"chess\",\"fishing\",\"betrayal\") or input a custom application ID as a string.")
