import boto3
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
import whisper
import srt
import datetime
import os
import sys
from dotenv import load_dotenv


# Loading environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Initialize the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name='us-east-1'
)


def download_from_s3(bucket, key, download_path):
    s3_client.download_file(bucket, key, download_path)

def upload_to_s3(upload_path, bucket, key):
    s3_client.upload_file(upload_path, bucket, key)

def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)

def transcribe_audio(audio_path, model_name="base"):
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path)
    return result

def convert_to_srt(transcription):
    subtitles = []
    for i, segment in enumerate(transcription['segments']):
        start_time = datetime.timedelta(seconds=segment['start'])
        end_time = datetime.timedelta(seconds=segment['end'])
        subtitles.append(srt.Subtitle(index=i, start=start_time, end=end_time, content=segment['text']))
    return srt.compose(subtitles)

def save_srt(srt_content, srt_path):
    with open(srt_path, 'w', encoding='utf-8') as file:
        file.write(srt_content)

def add_subtitles_to_video(video_path, srt_path):
    video = VideoFileClip(video_path)
    with open(srt_path, 'r', encoding='utf-8') as file:
        srt_content = file.read()
    subtitles = list(srt.parse(srt_content))
    clips = []
    for subtitle in subtitles:
        text_clip = TextClip(subtitle.content, font='Arial', fontsize=24, color='yellow', method='caption',
                             size=(video.w - 100, None), align='center', transparent=True)
        start = subtitle.start.total_seconds()
        end = subtitle.end.total_seconds()
        text_clip = text_clip.set_position(('center', 'bottom')).set_duration(end - start).set_start(start)
        clips.append(text_clip)
    video_with_subtitles = CompositeVideoClip([video] + clips)
    video_with_subtitles.write_videofile('output_with_subtitles.mp4')

def main(video_url):
    bucket_name = 'videobucketlegendario'
    video_key = video_url.split('/')[-1]
    video_path = video_key
    audio_path = 'audio.mp3'
    srt_path = 'output.srt'
    output_video_path = 'output_with_subtitles.mp4'
    output_video_key = 'processed/' + video_key

    download_from_s3(bucket_name, video_key, video_path)
    extract_audio(video_path, audio_path)
    transcription = transcribe_audio(audio_path)
    srt_content = convert_to_srt(transcription)
    save_srt(srt_content, srt_path)
    add_subtitles_to_video(video_path, srt_path)
    upload_to_s3('output_with_subtitles.mp4', "output-bucket-legendario", output_video_key)

if __name__ == "__main__":
    video_url = sys.argv[1] 
    main(video_url)