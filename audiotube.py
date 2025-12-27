import yt_dlp
import os

def download_youtube_audio(url, output_path="."):
    """
    Scarica l'audio di un video di YouTube alla massima qualità disponibile.

    Args:
        url (str): L'URL del video di YouTube.
        output_path (str): La directory dove salvare il file audio.
                           Default è la directory corrente.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ydl_opts = {
        'format': 'bestaudio/best',  # Seleziona la traccia audio migliore
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Estrai l'audio
            'preferredcodec': 'mp3',      # Converti in mp3
            'preferredquality': '320',    # Massima qualità (320kbps)
        }],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'), # Nome file di output
        'noplaylist': True,          # Scarica solo il singolo video, non l'intera playlist
        'geo_bypass': True,          # Bypass restrizioni geografiche
        'verbose': False,            # Disabilita output dettagliato (per un output più pulito)
        'progress_hooks': [lambda d: print(f"Stato: {d['status']}. {d.get('filename', '')}") if d['status'] == 'downloading' else None],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'unknown_video')
            print(f"Inizio download dell'audio per: '{video_title}'")
            ydl.download([url])
            print(f"Download completato per '{video_title}'. File salvato in '{output_path}'")
    except yt_dlp.utils.DownloadError as e:
        print(f"Errore durante il download: {e}")
    except Exception as e:
        print(f"Si è verificato un errore inaspettato: {e}")

if __name__ == "__main__":
    youtube_url = input("Inserisci l'URL del video di YouTube: ")
    download_folder = input("Inserisci il percorso della cartella di destinazione (premi Invio per la cartella corrente): ")

    if not download_folder:
        download_folder = "." # Usa la directory corrente se non specificata

    download_youtube_audio(youtube_url, download_folder)
