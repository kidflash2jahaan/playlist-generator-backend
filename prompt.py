import json
from openai import OpenAI
from dotenv import dotenv_values

client = OpenAI(api_key=dotenv_values(".env")["OPENAI_API_KEY"])

def get_playlist(prompt, count=8):
    messages = [
        {
            "role": "system",
            "content": 'You are a helpful playlist generating assistant. You should generate a list of songs and their artists according to a text prompt. The list has to have at least 2 songs. You should return a JSON array, where each element follows this format: {"song": <song_title>, "artist": <artist_name>}',
        },
        {
            "role": "user",
            "content": f"Gererate a playlist of {count} songs based on this prompt: {prompt}",
        },
    ]

    response = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
    )

    playlist = json.loads(response.choices[0].message.content)
    return playlist