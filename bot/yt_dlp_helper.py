import bot.yt_dlp_helper as yt_dlp_helper

ydl_opts = {}
with yt_dlp_helper.YoutubeDL(ydl_opts) as ydl:
    ydl.download(song_name)