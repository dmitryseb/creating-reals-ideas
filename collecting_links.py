from googleapiclient.discovery import build
from datetime import datetime, timedelta
import isodate
import os
from dotenv import load_dotenv
import json

from make_gpt_request import get_gpt_response

def make_queries_prompt(queries_number, topic):
   return f"I'm exploring YouTube Shorts (vertical videos under 1 minute) related to different topics. To get a better understanding of what's popular, I want to search for a variety of specific queries related to a given topic. In the end of this text I will give you a topic, you should generate a list of {str(queries_number)} specific hashtags that will help me discover the most popular and relevant videos. These tags together MUST cover all or almost all popular shorts which could potentially be created. Focus on how videos related to the topic might be titled, not just synonyms of the topic name. List the tags without numbering and without extra words. Separate them with a comma without any additional spaces etc. Don't use abstract names in square brackets, always use specific most popular examples instead of it. Avoid mentioning word news in your hashtags. Your topic for now is \"{topic}\". Create hashtags in the language in which topic is given."

def search_youtube_videos(youtube, query, max_results=20):
    one_month_ago = (datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SZ')

    request = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=max_results,
        type='video',
        publishedAfter=one_month_ago,
        order='viewCount',
        videoDuration='short',
        relevanceLanguage='en'
    )
    response = request.execute()

    videos = []
    for item in response['items']:
        video_id = item['id']['videoId']
        request = youtube.videos().list(
            part='snippet,statistics,contentDetails',
            id=video_id
        )
        info = request.execute()
        video = {
            'video_id': video_id,
            'url': f'https://www.youtube.com/watch?v={video_id}',
            'published_at': item['snippet']['publishedAt'],
            'view_count': get_views(info),
            'is_short': is_shorts_video(info),
            'thumbnail': info['items'][0]['snippet']['thumbnails']['high']['url'],
            'title': info['items'][0]['snippet']['title'],
            'description': info['items'][0]['snippet']['description']
        }
        videos.append(video)

    videos.sort(key=lambda x: int(x['view_count']), reverse=True)

    return videos

def get_views(info):
    return info['items'][0]['statistics']['viewCount']

def is_shorts_video(info):
    duration = info['items'][0]['contentDetails']['duration']
    duration_seconds = isodate.parse_duration(duration).total_seconds()

    return duration_seconds <= 120

def extract_shorts_links(videos):
    shorts_links = [(video['video_id'], video['url'], video['view_count'], video['thumbnail'], video['title'], video['description']) for video in videos if video['is_short']]
    return shorts_links

def generate_links_file(user_input):
    #user_input = input("Enter the topic for which you want to create a video (e.g., \"technology\"): ")
    tags_number = 3
    get_topics_prompt = make_queries_prompt(tags_number, user_input)
    tags = [user_input]
    tags += get_gpt_response(get_topics_prompt).split(",")
    for i in range(len(tags)):
        tags[i] = tags[i].strip()
        tags[i].replace(" ", "")
        if tags[i][0] == "#":
            tags[i] = tags[i][1:]
    tags = list(set(tags))
    if len(tags) > tags_number:
        tags = tags[:tags_number]
    print(tags)

    load_dotenv()

    key_number = int(os.getenv('KEY_NUMBER'))
    api_keys = [os.getenv('KEY_' + str(i)) for i in range(1, key_number + 1)]

    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    result = {"results": []}
    for tag in tags:
        for i in range(key_number):
            youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_keys[i])
            ok = False
            try:
                results = search_youtube_videos(youtube, query="#" + tag)
                print(f"Successfully proceeded query {tag} using {i}th key")
                ok = True
            except Exception as e:
                print(f"Error processing query {tag} using {i}th key, error: {e}")
                continue
            shorts_links = extract_shorts_links(results)
            res_now = {"query": tag, "videos": []}
            for link in shorts_links:
                res_now["videos"].append({"id": link[0], "link": link[1], "views": link[2], "thumbnail": link[3], "title": link[4], "description": link[5]})
            result["results"].append(res_now)
            if ok:
                break

    with open("links.json", "w") as json_file:
        json.dump(result, json_file, indent=4)