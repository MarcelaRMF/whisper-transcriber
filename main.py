from flask import Flask, request, jsonify
import yt_dlp
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/transcrever', methods=['POST'])
def transcrever():
    data = request.get_json()
    youtube_url = data.get('url')

    if not youtube_url:
        return jsonify({'error': 'URL do YouTube não fornecida.'}), 400

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        with open("audio.mp3", "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)

        return jsonify({'transcricao': transcript['text']})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)