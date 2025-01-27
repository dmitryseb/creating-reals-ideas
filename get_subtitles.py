from youtube_transcript_api import YouTubeTranscriptApi

def parse_video(video_id):
    subs = ""
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    for line in transcript:
        subs += line['text'] + " "
    return subs