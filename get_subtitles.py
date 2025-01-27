from youtube_transcript_api import YouTubeTranscriptApi

def parse_video(video_id):
    subs = ""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        for line in transcript:
            subs += line['text'] + " "
    except Exception as e:
        print(f"Subtitles for {video_id} not available: {e}")
        return
    print(subs)
    return subs