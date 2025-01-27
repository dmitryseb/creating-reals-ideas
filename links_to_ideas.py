import json
from get_subtitles import parse_video
from make_gpt_request import get_gpt_response

def trunc_str(string, length):
    return string[:length] if len(string) >= length else string

def generate_ideas():
    with open('links.json', 'r') as file:
        collected_data = json.load(file)

    with open("prompt_for_ideas.txt", "r") as f:
        prompt = f.read()
    videos = []
    for item in collected_data['results']:
        videos += item['videos']
    videos.sort(key=lambda v: int(v['views']), reverse=True)
    max_videos_number = 20
    i = 0
    cnt = 0
    while i < len(videos) and cnt < max_videos_number:
        subs = ""
        try:
            subs = parse_video(videos[i]['id'])
        except:
            pass
        if len(subs) < 100:
            i += 1
            continue
        prompt += f"Title: {trunc_str(videos[i]['title'], 100)}\n"
        #prompt += f"Description: {trunc_str(videos[i]['description'], 200)}\n"
        prompt += f"Views count: {videos[i]['views']}\n"
        prompt += "Transcription: "+ trunc_str(subs, 1500) + "\n"
        prompt += "\n"
        i += 1
        cnt += 1
        print(f"Successfully proceeded {i}th video")
    prompt = "".join([c if c.isascii() else "" for c in prompt])
    with open("generated_prompt.txt", "w") as f:
        f.write(prompt)
    result = get_gpt_response(prompt, 10000)
    return result
