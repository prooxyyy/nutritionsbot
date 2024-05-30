import time
import traceback

from openai import AsyncOpenAI
from aiogram import types

from cfg import cfg
from filters.ai_filters import PROCESSING

class AIManager:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=cfg['openai_key'])

    async def gpt(self, request: str, message: types.Message) -> str:
        user_id = message.from_user.username

        PROCESSING.append(message.from_user.id)

        try:
            completion = await self.client.chat.completions.create(
                model=cfg['openai_model'],
                messages=[
                    {"role": "system",
                     "content": "Your task is to generate a recipe for a healthy meal based on a list of foods that the user submits. The answer should be in Ukrainian."},
                    {"role": "user", "content": request},
                    {"role": "user",
                     "content": f"chat: {message.chat} Now {time.strftime('%d/%m/%Y %H:%M:%S')} user: {message.from_user.first_name} message: {request}"}
                ],
                max_tokens=600,
                user=user_id
            )
        except Exception:
            traceback.print_exc()
            PROCESSING.remove(message.from_user.id)
            raise

        chatgpt_response = completion.choices[0].message.content

        PROCESSING.remove(message.from_user.id)

        return chatgpt_response


    async def vision(self, photo_link: str, message: types.Message) -> str:
        user_id = message.from_user.username

        PROCESSING.append(message.from_user.id)

        try:
            completion = await self.client.chat.completions.create(
                model=cfg['openai_model'],
                messages=[
                    {"role": "system",
                     "content": "Your task is to generate a recipe for a healthy meal based on the list of products that are on the photo sent by the user. The answer must be in Ukrainian."},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": photo_link
                                }
                            }
                        ]
                    }
                ],
                max_tokens=600,
                temperature=1.0,
                frequency_penalty=0,
                presence_penalty=0,
                user=user_id
            )
        except Exception:
            PROCESSING.remove(message.from_user.id)
            raise

        chatgpt_response = completion.choices[0].message.content
        print(chatgpt_response)

        PROCESSING.remove(message.from_user.id)

        return chatgpt_response