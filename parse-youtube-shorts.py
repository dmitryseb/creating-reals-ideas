import yt_dlp
import re

url = 'https://www.youtube.com/shorts/Uf0XZ5kgB9Y'
ydl_opts = {
    'quiet': True,
    'writeautomaticsub': True,
    'writesubtitles': True,
    'subtitleslangs': ['ru'],
}


def clean_text(input_text):
    cleaned_text = re.sub(r'<.*?>', '', input_text)
    lines = cleaned_text.split('\n')
    unique_lines = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line and not line[
            0].isdigit() and stripped_line not in unique_lines:
            unique_lines.append(stripped_line)
    unique_lines = unique_lines[3:]
    return '\n'.join(unique_lines)


def extract_hashtags(text):
    hashtags = re.findall(r'#\w+', text)
    return hashtags


def extract_and_print_info(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=False)
        title = result.get('title')
        if title:
            print("Подпись к видео:")
            print(title)
        else:
            print("Подпись к видео отсутствует.")
        description = result.get('description')
        if description:
            print("\nОписание видео:")
            print(description)
        else:
            print("\nОписание видео отсутствует.")
        hashtags_from_title = extract_hashtags(title) if title else []
        hashtags_from_description = extract_hashtags(description) if description else []
        all_hashtags = list(set(hashtags_from_title + hashtags_from_description))
        if all_hashtags:
            print("\nХештеги из подписи и описания:")
            print(', '.join(all_hashtags))
        else:
            print("\nХештеги в подписи и описании отсутствуют.")
        subtitles = result.get('requested_subtitles')
        if subtitles:
            subtitle_url = subtitles.get('ru', {}).get('url')
            if subtitle_url:
                subtitle = ydl.urlopen(subtitle_url).read().decode('utf-8')
                print("\nСубтитры:")
                print(clean_text(subtitle))
            else:
                print("\nСубтитры на выбранном языке не найдены.")
        else:
            print("\nСубтитры для этого видео отсутствуют.")


extract_and_print_info(url)

