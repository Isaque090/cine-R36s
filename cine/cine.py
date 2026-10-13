import sys
import os
import json
import subprocess
import threading
import time
import hashlib
import urllib.request
import urllib.parse
import ssl
from datetime import datetime
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
try:
    import sdl2
    import sdl2.ext
    import sdl2.sdlttf as ttf
    from sdl2 import *
    try:
        import sdl2.sdlimage as sdlimage
        try:
            sdlimage.IMG_Init(sdlimage.IMG_INIT_JPG | sdlimage.IMG_INIT_PNG)
        except Exception:
            pass
        SDL_IMAGE_AVAILABLE = True
    except Exception:
        SDL_IMAGE_AVAILABLE = False
except ImportError as e:
    print(f"SDL2 Error: {e}")
    sys.exit(1)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
ssl._create_default_https_context = ssl._create_unverified_context
class Colors:
    BG_PRIMARY = (12, 18, 22)
    BG_SECONDARY = (20, 29, 34)
    BG_TERTIARY = (32, 44, 50)
    ACCENT = (1, 180, 228)
    MINT = (144, 206, 161)
    YT_RED = ACCENT  # Compatibility with existing controls and settings.
    TEXT_PRIMARY = (242, 247, 248)
    TEXT_SECONDARY = (184, 200, 207)
    TEXT_TERTIARY = (131, 154, 164)
    CARD_BG = (23, 33, 39)
    CARD_SELECTED = (32, 54, 63)
    NAV_BG = (17, 25, 30)
    NAV_ACTIVE = ACCENT
    NAV_INACTIVE = (131, 154, 164)
    STATUS_LOADING = MINT
    STATUS_ERROR = (255, 105, 105)
    STATUS_SUCCESS = MINT
    DIVIDER = (43, 59, 66)
    THUMB_BG = (27, 39, 46)
    PROGRESS_BG = (48, 65, 72)


# Translations
TRANSLATIONS = {
    "English": {
        # Navigation
        "nav_home": "Home",
        "nav_search": "Search",
        "nav_favorites": "Favs",
        "nav_history": "History",
        "nav_settings": "Settings",
        # Settings
        "settings_title": "Settings",
        "settings_language": "Language",
        "settings_quality": "Video Quality",
        "settings_full_screen": "Full Screen",
        "settings_video_height": "Video Height",
        "settings_search_count": "Search Count",
        "settings_auto_load": "Auto Load Home",
        "settings_trailer_id": "Trailer ID",
        "settings_clear_favorites": "Clear Favorites",
        "settings_clear_history": "Clear History",
        "settings_clear_cache": "Clear Thumb Cache",
        "settings_execute": "[A] Execute",
        "settings_on": "On",
        "settings_off": "Off",
        # Messages
        "msg_searching": "Searching videos...",
        "msg_loading": "Loading...",
        "msg_loading_video": "Loading Video...",
        "msg_loading_videos": "Loading videos...",
        "msg_no_results": "No results",
        "msg_press_search": "Press X to search",
        "msg_no_ytdlp": "yt-dlp not found!",
        "msg_no_tmdb_key": "TMDB key missing! Put it in config.txt",
        "msg_no_player": "No video player!",
        "msg_install_ytdlp": "Install: pip install yt-dlp",
        "msg_install_player": "Install: mpv or ffplay",
        "msg_timeout": "Timeout",
        "msg_added_fav": "Added to favorites",
        "msg_removed_fav": "Removed from favorites",
        "msg_fav_cleared": "Favorites cleared",
        "msg_history_cleared": "History cleared",
        "msg_cache_cleared": "Cache cleared",
        "msg_videos": "videos",
        # Help
        "help_keyboard": "A:Type  B:Close  START:Search",
        "help_main": "A:Select  B:Back  X:Search  Y:Fav  L/R:Tab",
        # Keyboard
        "kb_space": "SPACE",
        "kb_go": "GO",
        "kb_search_placeholder": "Type to search...",
        # Time
        "time_today": "Today",
        "time_live": "LIVE",
    },
    "Turkce": {
        # Navigation
        "nav_home": "Ana",
        "nav_search": "Ara",
        "nav_favorites": "Fav",
        "nav_history": "Gecmis",
        "nav_settings": "Ayarlar",
        # Settings
        "settings_title": "Ayarlar",
        "settings_language": "Dil",
        "settings_quality": "Video Kalitesi",
        "settings_full_screen": "Tam Ekran",
        "settings_video_height": "Video Yuksekligi",
        "settings_search_count": "Arama Sayisi",
        "settings_auto_load": "Otomatik Yukle",
        "settings_trailer_id": "Fragman ID",
        "settings_clear_favorites": "Favorileri Temizle",
        "settings_clear_history": "Gecmisi Temizle",
        "settings_clear_cache": "Onbellek Temizle",
        "settings_execute": "[A] Calistir",
        "settings_on": "Acik",
        "settings_off": "Kapali",
        # Messages
        "msg_searching": "Videolar araniyor...",
        "msg_loading": "Yukleniyor...",
        "msg_loading_video": "Video Yukleniyor...",
        "msg_loading_videos": "Videolar yukleniyor...",
        "msg_no_results": "Sonuc yok",
        "msg_press_search": "Aramak icin X'e bas",
        "msg_no_ytdlp": "yt-dlp bulunamadi!",
        "msg_no_player": "Video oynatici yok!",
        "msg_install_ytdlp": "Kur: pip install yt-dlp",
        "msg_install_player": "Kur: mpv veya ffplay",
        "msg_timeout": "Zaman asimi",
        "msg_added_fav": "Favorilere eklendi",
        "msg_removed_fav": "Favorilerden cikarildi",
        "msg_fav_cleared": "Favoriler temizlendi",
        "msg_history_cleared": "Gecmis temizlendi",
        "msg_cache_cleared": "Onbellek temizlendi",
        "msg_videos": "video",
        # Help
        "help_keyboard": "A:Yaz  B:Kapat  START:Ara",
        "help_main": "A:Sec  B:Geri  X:Ara  Y:Fav  L/R:Sekme",
        # Keyboard
        "kb_space": "BOSLUK",
        "kb_go": "GIT",
        "kb_search_placeholder": "Aramak icin yaz...",
        # Time
        "time_today": "Bugun",
        "time_live": "CANLI",
    },
    "Espanol": {
        # Navigation
        "nav_home": "Inicio",
        "nav_search": "Buscar",
        "nav_favorites": "Favs",
        "nav_history": "Historial",
        "nav_settings": "Ajustes",
        # Settings
        "settings_title": "Ajustes",
        "settings_language": "Idioma",
        "settings_quality": "Calidad Video",
        "settings_full_screen": "Pantalla Llena",
        "settings_video_height": "Altura Video",
        "settings_search_count": "Cant. Busqueda",
        "settings_auto_load": "Carga Auto",
        "settings_trailer_id": "ID Trailer",
        "settings_clear_favorites": "Borrar Favoritos",
        "settings_clear_history": "Borrar Historial",
        "settings_clear_cache": "Borrar Cache",
        "settings_execute": "[A] Ejecutar",
        "settings_on": "Si",
        "settings_off": "No",
        # Messages
        "msg_searching": "Buscando videos...",
        "msg_loading": "Cargando...",
        "msg_loading_video": "Cargando Video...",
        "msg_loading_videos": "Cargando videos...",
        "msg_no_results": "Sin resultados",
        "msg_press_search": "Pulsa X para buscar",
        "msg_no_ytdlp": "yt-dlp no encontrado!",
        "msg_no_player": "Sin reproductor!",
        "msg_install_ytdlp": "Instalar: pip install yt-dlp",
        "msg_install_player": "Instalar: mpv o ffplay",
        "msg_timeout": "Tiempo agotado",
        "msg_added_fav": "Agregado a favoritos",
        "msg_removed_fav": "Quitado de favoritos",
        "msg_fav_cleared": "Favoritos borrados",
        "msg_history_cleared": "Historial borrado",
        "msg_cache_cleared": "Cache borrado",
        "msg_videos": "videos",
        # Help
        "help_keyboard": "A:Escribir  B:Cerrar  START:Buscar",
        "help_main": "A:Elegir  B:Atras  X:Buscar  Y:Fav  L/R:Tab",
        # Keyboard
        "kb_space": "ESPACIO",
        "kb_go": "IR",
        "kb_search_placeholder": "Escribe para buscar...",
        # Time
        "time_today": "Hoy",
        "time_live": "VIVO",
    },
    "Portugues": {
        # Navigation
        "nav_home": "Inicio",
        "nav_search": "Buscar",
        "nav_favorites": "Favs",
        "nav_history": "Historico",
        "nav_settings": "Config",
        # Settings
        "settings_title": "Configuracoes",
        "settings_language": "Idioma",
        "settings_quality": "Qualidade Video",
        "settings_full_screen": "Tela Cheia",
        "settings_video_height": "Altura do Video",
        "settings_search_count": "Qtd. Busca",
        "settings_auto_load": "Carregar Auto",
        "settings_trailer_id": "ID do Trailer",
        "settings_clear_favorites": "Limpar Favoritos",
        "settings_clear_history": "Limpar Historico",
        "settings_clear_cache": "Limpar Cache",
        "settings_execute": "[A] Executar",
        "settings_on": "Sim",
        "settings_off": "Nao",
        # Messages
        "msg_searching": "Buscando videos...",
        "msg_loading": "Carregando...",
        "msg_loading_video": "Carregando Video...",
        "msg_loading_videos": "Carregando videos...",
        "msg_no_results": "Sem resultados",
        "msg_press_search": "Aperte X para buscar",
        "msg_no_ytdlp": "yt-dlp nao encontrado!",
        "msg_no_tmdb_key": "Chave TMDB faltando! Coloque no config.txt",
        "msg_no_player": "Sem reprodutor!",
        "msg_install_ytdlp": "Instalar: pip install yt-dlp",
        "msg_install_player": "Instalar: mpv ou ffplay",
        "msg_timeout": "Tempo esgotado",
        "msg_added_fav": "Adicionado aos favoritos",
        "msg_removed_fav": "Removido dos favoritos",
        "msg_fav_cleared": "Favoritos limpos",
        "msg_history_cleared": "Historico limpo",
        "msg_cache_cleared": "Cache limpo",
        "msg_videos": "videos",
        # Help
        "help_keyboard": "A:Digitar  B:Fechar  START:Buscar",
        "help_main": "A:Escolher  B:Voltar  X:Buscar  Y:Fav  L/R:Aba",
        # Keyboard
        "kb_space": "ESPACO",
        "kb_go": "IR",
        "kb_search_placeholder": "Digite para buscar...",
        # Time
        "time_today": "Hoje",
        "time_live": "AO VIVO",
    },
    "Deutsch": {
        # Navigation
        "nav_home": "Start",
        "nav_search": "Suche",
        "nav_favorites": "Favs",
        "nav_history": "Verlauf",
        "nav_settings": "Einst.",
        # Settings
        "settings_title": "Einstellungen",
        "settings_language": "Sprache",
        "settings_quality": "Videoqualitat",
        "settings_full_screen": "Vollbild",
        "settings_video_height": "Videohohe",
        "settings_search_count": "Suchanzahl",
        "settings_auto_load": "Auto Laden",
        "settings_trailer_id": "Trailer-ID",
        "settings_clear_favorites": "Favoriten loschen",
        "settings_clear_history": "Verlauf loschen",
        "settings_clear_cache": "Cache loschen",
        "settings_execute": "[A] Ausfuhren",
        "settings_on": "An",
        "settings_off": "Aus",
        # Messages
        "msg_searching": "Videos suchen...",
        "msg_loading": "Laden...",
        "msg_loading_video": "Video laden...",
        "msg_loading_videos": "Videos laden...",
        "msg_no_results": "Keine Ergebnisse",
        "msg_press_search": "X fur Suche drucken",
        "msg_no_ytdlp": "yt-dlp nicht gefunden!",
        "msg_no_player": "Kein Videoplayer!",
        "msg_install_ytdlp": "Installieren: pip install yt-dlp",
        "msg_install_player": "Installieren: mpv oder ffplay",
        "msg_timeout": "Zeituberschreitung",
        "msg_added_fav": "Zu Favoriten hinzugefugt",
        "msg_removed_fav": "Aus Favoriten entfernt",
        "msg_fav_cleared": "Favoriten geloscht",
        "msg_history_cleared": "Verlauf geloscht",
        "msg_cache_cleared": "Cache geloscht",
        "msg_videos": "Videos",
        # Help
        "help_keyboard": "A:Tippen  B:Schliessen  START:Suchen",
        "help_main": "A:Wahlen  B:Zuruck  X:Suche  Y:Fav  L/R:Tab",
        # Keyboard
        "kb_space": "LEER",
        "kb_go": "LOS",
        "kb_search_placeholder": "Zum Suchen tippen...",
        # Time
        "time_today": "Heute",
        "time_live": "LIVE",
    },
    "Francais": {
        # Navigation
        "nav_home": "Accueil",
        "nav_search": "Chercher",
        "nav_favorites": "Favs",
        "nav_history": "Historique",
        "nav_settings": "Params",
        # Settings
        "settings_title": "Parametres",
        "settings_language": "Langue",
        "settings_quality": "Qualite Video",
        "settings_full_screen": "Plein Ecran",
        "settings_video_height": "Hauteur Video",
        "settings_search_count": "Nb. Recherche",
        "settings_auto_load": "Charg. Auto",
        "settings_trailer_id": "ID Bande-ann.",
        "settings_clear_favorites": "Effacer Favoris",
        "settings_clear_history": "Effacer Historique",
        "settings_clear_cache": "Effacer Cache",
        "settings_execute": "[A] Executer",
        "settings_on": "Oui",
        "settings_off": "Non",
        # Messages
        "msg_searching": "Recherche videos...",
        "msg_loading": "Chargement...",
        "msg_loading_video": "Chargement Video...",
        "msg_loading_videos": "Chargement videos...",
        "msg_no_results": "Aucun resultat",
        "msg_press_search": "Appuyez X pour chercher",
        "msg_no_ytdlp": "yt-dlp non trouve!",
        "msg_no_player": "Pas de lecteur!",
        "msg_install_ytdlp": "Installer: pip install yt-dlp",
        "msg_install_player": "Installer: mpv ou ffplay",
        "msg_timeout": "Delai depasse",
        "msg_added_fav": "Ajoute aux favoris",
        "msg_removed_fav": "Retire des favoris",
        "msg_fav_cleared": "Favoris effaces",
        "msg_history_cleared": "Historique efface",
        "msg_cache_cleared": "Cache efface",
        "msg_videos": "videos",
        # Help
        "help_keyboard": "A:Taper  B:Fermer  START:Chercher",
        "help_main": "A:Choisir  B:Retour  X:Chercher  Y:Fav  L/R:Onglet",
        # Keyboard
        "kb_space": "ESPACE",
        "kb_go": "ALLER",
        "kb_search_placeholder": "Tapez pour chercher...",
        # Time
        "time_today": "Aujourd'hui",
        "time_live": "DIRECT",
    },
}

LANGUAGES = ["English", "Turkce", "Espanol", "Portugues", "Deutsch", "Francais"]

NAV_HOME = 0
NAV_SEARCH = 1
NAV_FAVORITES = 2
NAV_HISTORY = 3
NAV_SETTINGS = 4


def video_display_args(player_name, fill_screen, video_height="100%"):
    """Fullscreen player; optional reduced height in stretched/fill mode.

    Original-ratio mode remains unchanged. Reduced fill height adds centered
    black bars instead of cropping the movie. Values are language-independent.
    """
    allowed = {"100%": 100, "90%": 90, "80%": 80, "75%": 75}
    percent = allowed.get(video_height, 100)
    height = SCREEN_HEIGHT * percent // 100
    reduced = fill_screen and percent < 100
    canvas = (f"scale={SCREEN_WIDTH}:{height},setsar=1,"
              f"pad={SCREEN_WIDTH}:{SCREEN_HEIGHT}:0:(oh-ih)/2:black")
    if player_name == "mpv":
        args = ["--keepaspect=no" if fill_screen else "--keepaspect=yes",
                "--panscan=0", "--video-zoom=0", "--video-unscaled=no"]
        if reduced:
            args.append(f"--vf=lavfi=[{canvas}]")
        return args
    if player_name == "ffplay":
        args = ["-x", str(SCREEN_WIDTH), "-y", str(SCREEN_HEIGHT)]
        if fill_screen:
            args += ["-vf", canvas if reduced else
                     f"scale={SCREEN_WIDTH}:{SCREEN_HEIGHT},setsar=1"]
        return args
    if player_name == "vlc":
        # Fullscreen autoscale fits this ratio to screen width, adding bars.
        return [f"--aspect-ratio={SCREEN_WIDTH}:{height}" if fill_screen
                else "--aspect-ratio=", "--autoscale"]
    if player_name == "mplayer":
        args = ["-fs", "-zoom"]
        if fill_screen:
            args += ["-aspect", f"{SCREEN_WIDTH}:{SCREEN_HEIGHT}"]
            if reduced:
                args += ["-vf", f"scale={SCREEN_WIDTH}:{height},"
                         f"expand={SCREEN_WIDTH}:{SCREEN_HEIGHT}:-1:-1"]
        return args
    return []


def find_ytdlp():
    """yt-dlp binary'sini bul"""
    paths = [
        os.path.join(SCRIPT_DIR, "yt-dlp"),
        os.path.expanduser("~/.local/bin/yt-dlp"),
        "/home/ark/.local/bin/yt-dlp",
        "/usr/local/bin/yt-dlp",
        "/usr/bin/yt-dlp",
    ]
    
    for p in paths:
        if os.path.exists(p):
            try:
                os.chmod(p, 0o755)
            except:
                pass
            return p
    
    # PATH'te ara
    try:
        result = subprocess.run(["which", "yt-dlp"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except:
        pass
    
    return None


def find_video_player():
    """Video player bul"""
    players = ["mpv", "ffplay", "vlc", "mplayer"]
    
    for player in players:
        try:
            result = subprocess.run(["which", player], capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and result.stdout.strip():
                return player
        except:
            continue
    
    # PortMaster'da ffplay ara
    pm_ffplay = "/opt/system/Tools/PortMaster/libs/ffplay"
    if os.path.exists(pm_ffplay):
        return pm_ffplay
    
    return None


YTDLP_PATH = find_ytdlp()
VIDEO_PLAYER = find_video_player()


# === TMDB API ===
TMDB_API_BASE = "https://api.themoviedb.org/3"
TMDB_IMG_BASE = "https://image.tmdb.org/t/p/w185"

def load_tmdb_key():
    """Le a chave do TMDB do config.txt (linha TMDB_API_KEY=...)"""
    path = os.path.join(SCRIPT_DIR, "config.txt")
    try:
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("TMDB_API_KEY="):
                        return line.split("=", 1)[1].strip()
    except:
        pass
    return os.environ.get("TMDB_API_KEY", "")

TMDB_API_KEY = load_tmdb_key()

def load_config_value(name):
    path = os.path.join(SCRIPT_DIR, "config.txt")
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line.startswith(name + "="):
                    return line.split("=", 1)[1].strip()
    except Exception:
        pass
    return os.environ.get(name, "")

# Sua API de trailers. Use {tmdb_id} onde entra o id. Vazio = usa trailer do TMDB/YouTube.
TRAILER_API_URL = load_config_value("TRAILER_API_URL")

PROBE_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"

def probe_source(url, stype):
    """Testa se a fonte responde de verdade. Retorna (url_final, referer) ou None."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    refs = []
    try:
        q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        if q.get("referer"):
            refs.append(q["referer"][0])
    except Exception:
        pass
    if "streamtape" in url.lower():
        refs.append("https://streamtape.com/")
    refs += ["", "https://embedplayer2.xyz/"]
    seen = []
    for ref in refs:
        if ref in seen:
            continue
        seen.append(ref)
        headers = {"User-Agent": PROBE_UA, "Range": "bytes=0-2047"}
        if ref:
            headers["Referer"] = ref
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=12, context=ctx) as r:
                if r.status not in (200, 206):
                    continue
                data = r.read(2048)
                final = r.geturl()
                ctype = (r.headers.get("Content-Type") or "").lower()
            is_hls = stype == "hls" or ".m3u8" in final.lower() or b"#EXTM3U" in data[:64]
            if is_hls:
                if b"#EXTM3U" not in data[:64]:
                    continue
            else:
                if "text/html" in ctype or len(data) < 512 or data.lstrip()[:1] in (b"<", b"{"):
                    continue
            return final, ref
        except Exception as e:
            print(f"Probe falhou ({ref or 'sem referer'}): {url[:60]}... {e}")
    return None

_IMDB_CACHE = {}

def tmdb_to_imdb(tmdb_id):
    """Converte id do TMDB em id do IMDb (tt...) via TMDB external_ids. None se nao achar."""
    key = str(tmdb_id)
    if key in _IMDB_CACHE:
        return _IMDB_CACHE[key]
    data = tmdb_get(f"/movie/{key}/external_ids")
    imdb = (data or {}).get("imdb_id") or None
    if imdb:
        _IMDB_CACHE[key] = imdb
    return imdb

def build_trailer_api_url(tmdb_id, id_type="TMDB"):
    """Monta a URL da API de trailers mandando o id do TMDB ou do IMDb.
    Devolve (url, tipo_usado)."""
    use = "TMDB"
    value = str(tmdb_id)
    if str(id_type).upper() == "IMDB":
        imdb = tmdb_to_imdb(tmdb_id)
        if imdb:
            use, value = "IMDB", imdb
        else:
            print(f"IMDb id nao encontrado para TMDB {tmdb_id}, usando TMDB")
    q = urllib.parse.quote(value)
    base = TRAILER_API_URL
    if use == "IMDB":
        if "{imdb_id}" in base:
            url = base.replace("{imdb_id}", q)
        elif "tmdb_id={tmdb_id}" in base:
            url = base.replace("tmdb_id={tmdb_id}", "imdb_id=" + q)
        elif "{tmdb_id}" in base:
            url = base.replace("{tmdb_id}", q)
        else:
            url = base + ("&" if "?" in base else "?") + "imdb_id=" + q
    else:
        if "{tmdb_id}" in base:
            url = base.replace("{tmdb_id}", q)
        else:
            url = base + ("&" if "?" in base else "?") + "tmdb_id=" + q
    return url, use

def trailer_api_sources(tmdb_id, id_type="TMDB"):
    """Chama TRAILER_API_URL e devolve lista de {file,label,type}."""
    if not TRAILER_API_URL:
        return []
    url, used = build_trailer_api_url(tmdb_id, id_type)
    print(f"Trailer API ({used}): {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "CINE-R36S"})
        with urllib.request.urlopen(req, timeout=40) as r:
            data = json.loads(r.read().decode("utf-8", "ignore"))
        if not data.get("success"):
            return []
        return [x for x in data.get("sources", []) if isinstance(x, dict) and x.get("file")]
    except Exception as e:
        print(f"Trailer API error: {e}")
        return []

def tmdb_get(endpoint, params=None):
    """Chamada GET simples a API do TMDB. Retorna dict ou None."""
    if not TMDB_API_KEY:
        return None
    qs = f"api_key={TMDB_API_KEY}&language=pt-BR"
    if params:
        for k, v in params.items():
            qs += f"&{k}={urllib.parse.quote(str(v))}"
    url = f"{TMDB_API_BASE}{endpoint}?{qs}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "CINE-R36S/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"TMDB error: {e}")
        return None


class VideoItem:
    def __init__(self, data=None):
        if data:
            self.id = data.get('id', '')
            self.title = data.get('title', 'Unknown')
            self.channel = data.get('channel', data.get('uploader', 'Unknown'))
            self.duration = data.get('duration', 0)
            self.views = data.get('view_count', 0)
            self.upload_date = data.get('upload_date', '')
            self.url = data.get('webpage_url', data.get('url', f'https://www.youtube.com/watch?v={self.id}'))
            
            # Thumbnail URL - en iyi kaliteyi seç
            self.thumbnail = ''
            if data.get('thumbnail'):
                self.thumbnail = data.get('thumbnail')
            elif data.get('thumbnails'):
                thumbs = data.get('thumbnails', [])
                if thumbs:
                    # En küçük boyutlu thumbnail'i seç (daha hızlı yüklensin)
                    for t in thumbs:
                        if t.get('url'):
                            self.thumbnail = t.get('url')
                            break
            
            # YouTube default thumbnail
            if not self.thumbnail and self.id:
                self.thumbnail = f"https://i.ytimg.com/vi/{self.id}/mqdefault.jpg"
        else:
            self.id = ''
            self.title = ''
            self.channel = ''
            self.duration = 0
            self.views = 0
            self.thumbnail = ''
            self.upload_date = ''
            self.url = ''
    
    def format_duration(self):
        if not self.duration:
            return "LIVE"
        mins, secs = divmod(int(self.duration), 60)
        hours, mins = divmod(mins, 60)
        if hours:
            return f"{hours}:{mins:02d}:{secs:02d}"
        return f"{mins}:{secs:02d}"
    
    def format_views(self):
        if not self.views:
            return ""
        if self.views >= 1000000:
            return f"{self.views/1000000:.1f}M"
        if self.views >= 1000:
            return f"{self.views/1000:.1f}K"
        return str(self.views)
    
    def format_date(self):
        if not self.upload_date:
            return ""
        try:
            date = datetime.strptime(self.upload_date, "%Y%m%d")
            delta = datetime.now() - date
            if delta.days < 1:
                return "Today"
            if delta.days < 7:
                return f"{delta.days}d"
            if delta.days < 30:
                return f"{delta.days // 7}w"
            if delta.days < 365:
                return f"{delta.days // 30}mo"
            return f"{delta.days // 365}y"
        except:
            return ""
    
    @classmethod
    def from_tmdb(cls, movie):
        """Cria VideoItem a partir de um filme do TMDB"""
        v = cls()
        v.id = str(movie.get('id', ''))
        v.title = movie.get('title') or movie.get('name') or 'Unknown'
        release = movie.get('release_date') or ''
        year = release[:4] if release else ''
        votes = movie.get('vote_average', 0)
        v.channel = f"{year}  ★ {votes:.1f}" if year else f"★ {votes:.1f}"
        v.duration = 0
        v.views = movie.get('vote_count', 0)
        v.upload_date = release.replace('-', '') if release else ''
        poster = movie.get('poster_path') or movie.get('backdrop_path') or ''
        v.thumbnail = f"{TMDB_IMG_BASE}{poster}" if poster else ''
        v.url = f"tmdb://{v.id}"
        return v

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'channel': self.channel,
            'duration': self.duration,
            'view_count': self.views,
            'thumbnail': self.thumbnail,
            'upload_date': self.upload_date,
            'url': self.url
        }


class CineApp:
    def __init__(self):
        SDL_Init(SDL_INIT_VIDEO | SDL_INIT_JOYSTICK | SDL_INIT_GAMECONTROLLER)
        ttf.TTF_Init()
        
        self.window = SDL_CreateWindow(
            b"CINE R36S",
            SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
            SCREEN_WIDTH, SCREEN_HEIGHT,
            SDL_WINDOW_SHOWN
        )
        self.renderer = SDL_CreateRenderer(self.window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)
        SDL_SetRenderDrawBlendMode(self.renderer, SDL_BLENDMODE_BLEND)
        
        # Controller
        self.controller = None
        self.joystick = None
        if SDL_NumJoysticks() > 0:
            if SDL_IsGameController(0):
                self.controller = SDL_GameControllerOpen(0)
            else:
                self.joystick = SDL_JoystickOpen(0)
        
        # Font
        font_path = self._find_font()
        self.font = self.font_large = self.font_small = self.font_tiny = None
        if font_path:
            self.font = ttf.TTF_OpenFont(font_path.encode(), 18)
            self.font_large = ttf.TTF_OpenFont(font_path.encode(), 24)
            self.font_small = ttf.TTF_OpenFont(font_path.encode(), 14)
            self.font_tiny = ttf.TTF_OpenFont(font_path.encode(), 12)
        
        # Caches
        self.text_cache = {}
        self.image_cache = {}
        self.failed_images = set()
        self.loading_images = set()
        self.image_cache_dir = os.path.join(SCRIPT_DIR, ".thumb_cache")
        os.makedirs(self.image_cache_dir, exist_ok=True)
        
        if SDL_IMAGE_AVAILABLE:
            try:
                sdlimage.IMG_Init(sdlimage.IMG_INIT_JPG | sdlimage.IMG_INIT_PNG)
            except:
                pass
        
        # State
        self.running = True
        self.need_redraw = True
        self.frame_count = 0
        
        self.current_nav = NAV_HOME
        self.selected = 0
        self.scroll = 0
        
        self.ytdlp_path = YTDLP_PATH
        self.video_player = VIDEO_PLAYER
        
        # Data
        self.home_videos = []
        self.search_results = []
        self.favorites = self._load_json("yt_favorites.json")
        self.history = self._load_json("yt_history.json")
        self.last_search_query = ""
        self.home_page = 0
        self.search_page = 0
        self.max_videos = 50  # Maksimum video sayısı
        
        # Batch tracking
        self.home_batch = 1
        self.search_batch = 1
        self.home_batch_loading = False
        self.search_batch_loading = False
        self.home_first_batch_count = 0
        self.search_first_batch_count = 0
        self.home_existing_ids = set()
        self.search_existing_ids = set()
        
        # Settings
        self.settings = self._load_settings()
        self._update_settings_items()
        self.settings_selected = 0
        self.settings_scroll = 0
        
        # Status
        status_parts = []
        if TMDB_API_KEY:
            status_parts.append("TMDB OK")
        else:
            status_parts.append("NO TMDB key!")
        if self.video_player:
            status_parts.append(f"Player: {os.path.basename(self.video_player)}")
        else:
            status_parts.append("NO player!")

        self.status = " | ".join(status_parts)
        self.status_type = "ok" if TMDB_API_KEY else "error"
        self.is_loading = False
        
        # Keyboard
        self.search_active = False
        self.search_query = ""
        self.keyboard_row = 0
        self.keyboard_col = 0
        self.caps_lock = False
        self.keyboard_layout = [
            list("1234567890"),
            list("qwertyuiop"),
            list("asdfghjkl"),
            list("zxcvbnm"),
        ]
        
        # Input
        self.key_held = None
        self.key_hold_start = 0
        self.last_repeat = 0
        
        # Playback
        self.is_playing = False
        self.is_loading_video = False
        self.is_searching = False
        self.player_process = None
        self.current_video = None
        self.player_paused = False
        self.mpv_socket = None
        
        # Loading spinner sticky flag
        self.loading_spinner_triggered = False
        
        print(f"yt-dlp: {self.ytdlp_path}")
        print(f"Player: {self.video_player}")
    
    def _find_font(self):
        paths = [
            os.path.join(SCRIPT_DIR, "font.ttf"),
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/TTF/DejaVuSans.ttf",
            "/opt/system/Tools/PortMaster/themes/default.ttf",
        ]
        for p in paths:
            if os.path.exists(p):
                return p
        return None
    
    def _load_json(self, filename):
        try:
            path = os.path.join(SCRIPT_DIR, filename)
            if os.path.exists(path):
                with open(path) as f:
                    return [VideoItem(v) for v in json.load(f)]
        except Exception as e:
            print(f"Load {filename} error: {e}")
        return []
    
    def _save_json(self, filename, items):
        try:
            path = os.path.join(SCRIPT_DIR, filename)
            with open(path, 'w') as f:
                json.dump([v.to_dict() for v in items[:50]], f)
        except Exception as e:
            print(f"Save {filename} error: {e}")
    
    def _load_settings(self):
        try:
            path = os.path.join(SCRIPT_DIR, "yt_settings.json")
            if os.path.exists(path):
                with open(path) as f:
                    settings = json.load(f)
                    settings.setdefault("full_screen", "On")
                    settings.setdefault("video_height", "100%")
                    settings.setdefault("trailer_id", "TMDB")
                    return settings
        except:
            pass
        return {
            "quality": "480p",
            "full_screen": "On",
            "video_height": "100%",
            "search_count": "10",
            "auto_load": "On",
            "trailer_id": "TMDB",
            "language": "English"
        }
    
    def _save_settings(self):
        try:
            path = os.path.join(SCRIPT_DIR, "yt_settings.json")
            with open(path, 'w') as f:
                json.dump(self.settings, f)
        except:
            pass
    
    def t(self, key):
        """Get translated string for current language"""
        lang = self.settings.get("language", "English")
        if lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
            return TRANSLATIONS[lang][key]
        # Fallback to English
        return TRANSLATIONS["English"].get(key, key)
    
    def _update_settings_items(self):
        """Update settings items with current language"""
        lang = self.settings.get("language", "English")
        tr = TRANSLATIONS.get(lang, TRANSLATIONS["English"])
        
        on_off = [tr["settings_on"], tr["settings_off"]]
        
        self.settings_items = [
            (tr["settings_language"], "language", LANGUAGES),
            (tr["settings_quality"], "quality", ["360p", "480p", "720p"]),
            (tr["settings_full_screen"], "full_screen", on_off),
            (tr["settings_video_height"], "video_height", ["100%", "90%", "80%", "75%"]),
            (tr["settings_search_count"], "search_count", ["10", "15", "20", "25"]),
            (tr["settings_auto_load"], "auto_load", on_off),
            (tr.get("settings_trailer_id", TRANSLATIONS["English"]["settings_trailer_id"]), "trailer_id", ["TMDB", "IMDb"]),
            (tr["settings_clear_favorites"], "clear_favorites", None),
            (tr["settings_clear_history"], "clear_history", None),
            (tr["settings_clear_cache"], "clear_cache", None),
        ]
    
    def add_to_history(self, video):
        self.history = [v for v in self.history if v.id != video.id]
        self.history.insert(0, video)
        self._save_json("yt_history.json", self.history)
    
    # === TMDB API ===
    def search_youtube(self, query):
        if not TMDB_API_KEY:
            self.status = self.t("msg_no_tmdb_key")
            self.status_type = "error"
            self.need_redraw = True
            return
        
        count = int(self.settings.get("search_count", "8"))
        self.last_search_query = query
        self.search_batch = 1
        self.search_existing_ids = set()
        self.search_first_batch_count = 0
        
        # Listeyi temizle ve hemen search sayfasına geç
        self.search_results = []
        self.selected = 0
        self.scroll = 0
        self.current_nav = NAV_SEARCH
        self.search_active = False
        
        self.is_loading = True
        self.is_searching = True  # Searching loading ekranı için
        self.status = "Searching..."
        self.status_type = "loading"
        self.need_redraw = True
        
        # İlk batch'i yükle
        self._load_batch("search", 1)
    
    def _load_batch(self, list_type, batch_num):
        """Belirli bir batch'i yükle"""
        count = int(self.settings.get("search_count", "8"))
        
        if list_type == "search":
            if self.search_batch_loading:
                return
            self.search_batch_loading = True
            target_list = self.search_results
            existing_ids = self.search_existing_ids
        else:
            if self.home_batch_loading:
                return
            self.home_batch_loading = True
            target_list = self.home_videos
            existing_ids = self.home_existing_ids

        def worker():
            try:
                # Cada batch = uma pagina da API do TMDB
                if list_type == "search":
                    data = tmdb_get("/search/movie", {
                        "query": self.last_search_query,
                        "page": batch_num,
                        "include_adult": "false",
                    })
                else:
                    data = tmdb_get("/trending/movie/week", {"page": batch_num})

                added = 0
                if data:
                    for movie in data.get("results", []):
                        vid_id = str(movie.get('id', ''))
                        if vid_id and vid_id not in existing_ids:
                            video = VideoItem.from_tmdb(movie)
                            target_list.append(video)
                            existing_ids.add(vid_id)
                            added += 1
                
                # Batch numarasını güncelle
                if list_type == "search":
                    self.search_batch = batch_num
                    self.search_batch_loading = False
                    if batch_num == 1:
                        self.search_first_batch_count = len(target_list)
                else:
                    self.home_batch = batch_num
                    self.home_batch_loading = False
                    if batch_num == 1:
                        self.home_first_batch_count = len(target_list)
                
                # Yükleme bittiğinde spinner flag'ini sıfırla
                self.loading_spinner_triggered = False
                
                if target_list:
                    self.status = f"{len(target_list)} videos"
                    self.status_type = "ok"
                else:
                    self.status = "No results" if list_type == "search" else "Press X to search"
                    self.status_type = "error" if list_type == "search" else "ok"
                
                # İlk batch ise loading'i kapat
                if batch_num == 1:
                    self.is_loading = False
                    if list_type == "search":
                        self.is_searching = False  # Arama loading ekranını kapat
                    # 1 saniye sonra ikinci batch'i yükle
                    if target_list:
                        threading.Timer(1.0, lambda: self._load_batch(list_type, 2)).start()
                
                self.need_redraw = True
                
            except subprocess.TimeoutExpired:
                if batch_num == 1:
                    self.status = "Timeout"
                    self.status_type = "error"
                    self.is_loading = False
                    if list_type == "search":
                        self.is_searching = False
                if list_type == "search":
                    self.search_batch_loading = False
                else:
                    self.home_batch_loading = False
                self.need_redraw = True
            except Exception as e:
                if batch_num == 1:
                    self.status = f"Error: {str(e)[:20]}"
                    self.status_type = "error"
                    self.is_loading = False
                    if list_type == "search":
                        self.is_searching = False
                if list_type == "search":
                    self.search_batch_loading = False
                else:
                    self.home_batch_loading = False
                self.need_redraw = True
        
        threading.Thread(target=worker, daemon=True).start()
    
    def check_load_next_batch(self):
        """Kullanıcı scroll yaptığında sonraki batch'i yükle"""
        if self.current_nav == NAV_HOME:
            # İkinci batch'in ilk videosuna ulaşıldı mı?
            if (self.home_batch == 2 and 
                self.selected >= self.home_first_batch_count and 
                not self.home_batch_loading and
                len(self.home_videos) < self.max_videos):
                self._load_batch("home", 3)
            # 3. batch'ten sonra her batch için
            elif (self.home_batch >= 3 and
                  self.selected >= len(self.home_videos) - 3 and
                  not self.home_batch_loading and
                  len(self.home_videos) < self.max_videos):
                self._load_batch("home", self.home_batch + 1)
                
        elif self.current_nav == NAV_SEARCH:
            # İkinci batch'in ilk videosuna ulaşıldı mı?
            if (self.search_batch == 2 and
                self.selected >= self.search_first_batch_count and
                not self.search_batch_loading and
                len(self.search_results) < self.max_videos):
                self._load_batch("search", 3)
            # 3. batch'ten sonra her batch için
            elif (self.search_batch >= 3 and
                  self.selected >= len(self.search_results) - 3 and
                  not self.search_batch_loading and
                  len(self.search_results) < self.max_videos):
                self._load_batch("search", self.search_batch + 1)
    
    def load_trending(self):
        if not TMDB_API_KEY:
            return
        
        if self.settings.get("auto_load") == "Off":
            return
        
        self.home_batch = 1
        self.home_existing_ids = set()
        self.home_first_batch_count = 0
        self.home_videos = []  # Listeyi temizle
        self.is_loading = True
        self.status = "Loading..."
        self.status_type = "loading"
        self.need_redraw = True
        self.render()
        
        # İlk batch'i yükle
        self._load_batch("home", 1)
    
    def render_loading_screen(self, title="Loading...", subtitle=""):
        self.draw_rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, Colors.BG_PRIMARY)
        self.render_header()
        self.draw_text("CINE R36S", 244, 138, Colors.MINT, self.font_large)
        self.draw_spinner(SCREEN_WIDTH // 2, 200, radius=18, dot_size=4)
        self.draw_centered_text(title, 238, Colors.TEXT_PRIMARY, self.font, 596)
        if subtitle:
            self.draw_centered_text(subtitle, 274, Colors.TEXT_SECONDARY, self.font_small, 560)
        self.draw_rect(220, 326, 200, 3, Colors.PROGRESS_BG)
        position = (SDL_GetTicks() // 10) % 160
        self.draw_rect(220 + position, 326, 40, 3, Colors.ACCENT)
        SDL_RenderPresent(self.renderer)
        self.frame_count += 1

    
    def play_video(self, video):
        if not self.ytdlp_path and not TRAILER_API_URL:
            self.status = "yt-dlp not found!"
            self.status_type = "error"
            return
        
        if not self.video_player:
            self.status = "No video player found!"
            self.status_type = "error"
            return
        
        self.add_to_history(video)
        self.current_video = video
        self.is_loading_video = True
        self.status = "Loading video..."
        self.status_type = "loading"
        self.need_redraw = True
        
        # Loading ekranını göster
        self.render_loading_screen(self.t("msg_loading_video"), video.title)
        
        # Kalite ayarını al
        quality = self.settings.get("quality", "480p")
        height = quality.replace("p", "")
        
        def worker():
            try:
                stream_url = None
                stream_type = ""
                stream_referer = ""
                page_url = video.url
                # 1) Sua API de trailers (TRAILER_API_URL no config.txt)
                if page_url.startswith("tmdb://") and TRAILER_API_URL:
                    self.status = "Consultando API de trailers..."
                    self.need_redraw = True
                    sources = trailer_api_sources(page_url.split("://", 1)[1], self.settings.get("trailer_id", "TMDB"))
                    if sources:
                        def _prio(x):
                            t = str(x.get("type", "")).lower()
                            f = str(x.get("file", "")).lower()
                            # HLS direto primeiro, depois HLS via proxy, depois mp4/streamtape
                            if t == "hls" and "hls.php" not in f:
                                return 0
                            if t == "hls":
                                return 1
                            if "streamtape" in f:
                                return 3
                            return 2
                        sources = sorted(sources, key=_prio)
                        total = len(sources)
                        for i, src in enumerate(sources, 1):
                            self.status = f"Testando {src.get('label', 'fonte')} ({i}/{total})..."
                            self.need_redraw = True
                            st = str(src.get("type", "")).lower()
                            res = probe_source(src["file"], st)
                            if res:
                                stream_url, stream_referer = res
                                stream_type = "hls" if (st == "hls" or ".m3u8" in stream_url.lower()) else "direct"
                                print(f"Fonte OK: {src.get('label')} -> {stream_url[:80]}")
                                break
                        if not stream_url:
                            self.status = "Nenhuma fonte da API funcionou"
                            self.need_redraw = True

                # 1b) URL direta de video (ex.: Streamtape get_video, .mp4, .m3u8)
                if not stream_url and not page_url.startswith("tmdb://"):
                    low = page_url.lower()
                    if ("get_video" in low or low.split("?")[0].endswith((".mp4", ".m3u8", ".mkv", ".webm"))):
                        st = "hls" if ".m3u8" in low else "direct"
                        res = probe_source(page_url, st)
                        stream_url, stream_referer = res if res else (page_url, "")
                        stream_type = st

                if not stream_url and not self.ytdlp_path:
                    self.status = "Nenhum trailer na API"
                    self.status_type = "error"
                    self.is_loading_video = False
                    self.need_redraw = True
                    return
                # 2) Sem resultado: trailer (YouTube) pela API do TMDB
                if not stream_url and page_url.startswith("tmdb://"):
                    tmdb_id = page_url.split("://", 1)[1]
                    vids = tmdb_get(f"/movie/{tmdb_id}/videos")
                    if not vids or not vids.get("results"):
                        # Tenta sem filtro de idioma
                        vids = tmdb_get(f"/movie/{tmdb_id}/videos", {"language": "en-US"})
                    yt_key = None
                    if vids:
                        results = [v for v in vids.get("results", []) if v.get("site") == "YouTube"]
                        # Prefere Trailer oficial, depois Teaser, depois qualquer um
                        for want in ("Trailer", "Teaser", "Clip"):
                            for v in results:
                                if v.get("type") == want:
                                    yt_key = v.get("key")
                                    break
                            if yt_key:
                                break
                        if not yt_key and results:
                            yt_key = results[0].get("key")
                    if not yt_key:
                        self.status = "No trailer found"
                        self.status_type = "error"
                        self.is_loading_video = False
                        self.need_redraw = True
                        return
                    page_url = f"https://www.youtube.com/watch?v={yt_key}"

                if not stream_url:
                    # Video URL al
                    cmd = [
                        self.ytdlp_path,
                        "-f", f"best[height<={height}]/best",
                        "-g",
                        "--no-warnings",
                        "--no-check-certificates",
                        "--no-playlist",
                        page_url
                    ]
                
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                    if result.returncode != 0:
                        self.status = "Failed to get URL"
                        self.status_type = "error"
                        self.is_loading_video = False
                        self.need_redraw = True
                        return
                
                    stream_url = result.stdout.strip().split('\n')[0]
                
                if not stream_url:
                    self.status = "No stream URL"
                    self.status_type = "error"
                    self.is_loading_video = False
                    self.need_redraw = True
                    return
                
                self.is_loading_video = False
                
                # SDL penceresini gizle
                SDL_HideWindow(self.window)
                
                self.is_playing = True
                self.player_paused = False
                
                player = self.video_player
                player_name = os.path.basename(player)
                
                # mpv için IPC socket
                self.mpv_socket = f"/tmp/mpv_{os.getpid()}"
                
                if player_name == "mpv":
                    player_cmd = [
                        player,
                        "--fs",
                        "--no-terminal",
                        "--really-quiet",
                        f"--input-ipc-server={self.mpv_socket}",
                        "--osd-level=1",
                        "--osd-duration=1500",
                        "--cache=yes",
                        "--cache-secs=30",
                        "--demuxer-max-bytes=50M",
                        "--demuxer-readahead-secs=20",
                        "--hwdec=auto-safe",
                        "--profile=fast",
                        "--video-latency-hacks=yes",
                    ]
                    if stream_type == "hls" or ".m3u8" in str(stream_url):
                        player_cmd.append("--demuxer-lavf-o=protocol_whitelist=[file,http,https,tcp,tls,crypto]")
                        player_cmd.append("--hls-bitrate=min")
                    if stream_type in ("hls", "direct"):
                        player_cmd.append(f"--user-agent={PROBE_UA}")
                        if stream_referer:
                            player_cmd.append(f"--referrer={stream_referer}")
                    player_cmd.append(stream_url)
                elif player_name == "ffplay":
                    player_cmd = [player, "-fs", "-autoexit", "-loglevel", "quiet"]
                    if stream_type in ("hls", "direct"):
                        player_cmd += ["-user_agent", PROBE_UA]
                        if stream_referer:
                            player_cmd += ["-headers", f"Referer: {stream_referer}\r\n"]
                    player_cmd.append(stream_url)
                elif player_name == "vlc":
                    player_cmd = [player, "--fullscreen", "--play-and-exit", "-q"]
                    if stream_type in ("hls", "direct"):
                        player_cmd.append(f"--http-user-agent={PROBE_UA}")
                        if stream_referer:
                            player_cmd.append(f"--http-referrer={stream_referer}")
                    player_cmd.append(stream_url)
                else:
                    player_cmd = [player, stream_url]

                # Insert options before the URL for every supported player.
                display_args = video_display_args(
                    player_name, self.settings.get("full_screen", "On") == "On",
                    self.settings.get("video_height", "100%"))
                player_cmd[-1:-1] = display_args

                self.player_process = subprocess.Popen(
                    player_cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                
                self.player_process.wait()
                
            except Exception as e:
                print(f"Play error: {e}")
            finally:
                self.is_playing = False
                self.player_process = None
                self.current_video = None
                self.player_paused = False
                
                # Socket temizle
                try:
                    if hasattr(self, 'mpv_socket') and self.mpv_socket and os.path.exists(self.mpv_socket):
                        os.remove(self.mpv_socket)
                except:
                    pass
                
                # SDL penceresini göster
                SDL_ShowWindow(self.window)
                SDL_RaiseWindow(self.window)
                
                self.status = "Ready"
                self.status_type = "ok"
                self.need_redraw = True
        
        threading.Thread(target=worker, daemon=True).start()
    
    def send_mpv_command(self, command):
        """mpv'ye IPC komutu gönder - sessizce"""
        if not self.is_playing or not hasattr(self, 'mpv_socket') or not self.mpv_socket:
            return False
        
        try:
            import socket
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            sock.connect(self.mpv_socket)
            sock.send((json.dumps({"command": command}) + "\n").encode())
            sock.close()
            return True
        except:
            return False
    
    def player_seek(self, seconds):
        """Video'da ileri/geri sar - render tetiklemeden"""
        if self.is_playing:
            self.send_mpv_command(["seek", str(seconds), "relative"])
    
    def player_toggle_pause(self):
        """Duraklat/devam - render tetiklemeden"""
        if self.is_playing:
            self.send_mpv_command(["cycle", "pause"])
    
    def player_brightness(self, delta):
        """Parlaklık ayarla"""
        if self.is_playing:
            self.send_mpv_command(["add", "brightness", str(delta)])
    
    def stop_playback(self):
        if self.player_process:
            try:
                self.player_process.terminate()
                self.player_process.wait(timeout=2)
            except:
                try:
                    self.player_process.kill()
                except:
                    pass
        
        self.is_playing = False
        self.player_process = None
        self.current_video = None
        
        # SDL penceresini göster
        SDL_ShowWindow(self.window)
        SDL_RaiseWindow(self.window)
        
        self.status = "Stopped"
        self.status_type = "ok"
        self.need_redraw = True
    
    # === Thumbnail ===
    def get_thumb_path(self, url):
        h = hashlib.md5(url.encode()).hexdigest()
        return os.path.join(self.image_cache_dir, f"{h}.jpg")
    
    def download_thumbnail(self, url):
        if not url or url in self.failed_images or url in self.loading_images:
            return
        
        # Aynı anda maksimum 3 indirme
        if len(self.loading_images) >= 6:
            return
        
        self.loading_images.add(url)
        
        def worker():
            try:
                cache_path = self.get_thumb_path(url)
                
                if os.path.exists(cache_path):
                    self.loading_images.discard(url)
                    self.need_redraw = True
                    return
                
                # URL'yi düzelt
                download_url = url
                if download_url.startswith("//"):
                    download_url = "https:" + download_url
                
                req = urllib.request.Request(download_url, headers={
                    'User-Agent': 'Mozilla/5.0'
                })
                
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                
                with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
                    data = resp.read()
                    if len(data) > 500:
                        with open(cache_path, 'wb') as f:
                            f.write(data)
                    else:
                        self.failed_images.add(url)
                
            except:
                self.failed_images.add(url)
            finally:
                self.loading_images.discard(url)
                self.need_redraw = True
        
        threading.Thread(target=worker, daemon=True).start()
    
    def load_thumbnail(self, url):
        if not url:
            return None
        
        # Cache'de var mı?
        if url in self.image_cache:
            return self.image_cache[url]
        
        # Başarısız mı?
        if url in self.failed_images:
            return None
        
        # Dosya var mı?
        cache_path = self.get_thumb_path(url)
        if os.path.exists(cache_path) and SDL_IMAGE_AVAILABLE:
            try:
                surface = sdlimage.IMG_Load(cache_path.encode())
                if surface:
                    texture = SDL_CreateTextureFromSurface(self.renderer, surface)
                    w, h = surface.contents.w, surface.contents.h
                    SDL_FreeSurface(surface)
                    if texture:
                        # Cache limit
                        if len(self.image_cache) > 30:
                            old_key = next(iter(self.image_cache))
                            old_tex = self.image_cache.pop(old_key)
                            if old_tex and old_tex[0]:
                                SDL_DestroyTexture(old_tex[0])
                        
                        self.image_cache[url] = (texture, w, h)
                        return (texture, w, h)
            except Exception as e:
                print(f"Load thumbnail error: {e}")
        
        # İndir
        if url not in self.loading_images:
            self.download_thumbnail(url)
        
        return None
    
    def draw_thumbnail(self, x, y, width, height, url):
        # Background
        self.draw_rect(x, y, width, height, Colors.THUMB_BG)
        
        if not url:
            return
        
        result = self.load_thumbnail(url)
        if result:
            texture, img_w, img_h = result
            if texture:
                # Aspect fit
                aspect = img_w / img_h if img_h else 16/9
                target_aspect = width / height
                
                if aspect > target_aspect:
                    draw_w = width
                    draw_h = int(width / aspect)
                    draw_x = x
                    draw_y = y + (height - draw_h) // 2
                else:
                    draw_h = height
                    draw_w = int(height * aspect)
                    draw_x = x + (width - draw_w) // 2
                    draw_y = y
                
                dst = SDL_Rect(int(draw_x), int(draw_y), int(draw_w), int(draw_h))
                SDL_RenderCopy(self.renderer, texture, None, dst)
                return
        
        # Loading indicator
        if url in self.loading_images:
            dots = "." * ((self.frame_count // 20) % 4)
            self.draw_text(dots, x + width//2 - 10, y + height//2 - 5, Colors.TEXT_SECONDARY, self.font_small)
    
    # === Drawing ===
    def draw_rect(self, x, y, w, h, color, alpha=255):
        SDL_SetRenderDrawColor(self.renderer, color[0], color[1], color[2], alpha)
        SDL_RenderFillRect(self.renderer, SDL_Rect(int(x), int(y), int(w), int(h)))
    
    def draw_spinner(self, center_x, center_y, radius=12, dot_size=3):
        """Dönen nokta animasyonu çiz - saat yönünde 8 pozisyon"""
        # 8 pozisyon (saat yönünde: 12, 1:30, 3, 4:30, 6, 7:30, 9, 10:30)
        import math
        positions = []
        for i in range(8):
            angle = math.pi / 2 - (i * math.pi / 4)  # 12'den başla, saat yönünde
            px = center_x + int(radius * math.cos(angle))
            py = center_y - int(radius * math.sin(angle))
            positions.append((px, py))
        
        # Aktif nokta indeksi (animasyon)
        active_index = (self.frame_count // 6) % 8
        
        # Noktaları çiz
        for i, (px, py) in enumerate(positions):
            if i == active_index:
                # Aktif nokta - büyük ve parlak kırmızı
                self.draw_rect(px - dot_size, py - dot_size, dot_size * 2, dot_size * 2, Colors.YT_RED)
            else:
                # Pasif nokta - küçük ve soluk
                self.draw_rect(px - 1, py - 1, 2, 2, Colors.TEXT_TERTIARY)
    
    def draw_text(self, text, x, y, color=Colors.TEXT_PRIMARY, font=None):
        if not font:
            font = self.font
        if not font:
            return 0
        
        text = str(text)[:80]
        key = (text, color, id(font))
        
        if key not in self.text_cache:
            if len(self.text_cache) > 150:
                for tex, _, _ in self.text_cache.values():
                    if tex:
                        SDL_DestroyTexture(tex)
                self.text_cache.clear()
            
            sdl_color = SDL_Color(color[0], color[1], color[2], 255)
            surface = ttf.TTF_RenderUTF8_Blended(font, text.encode('utf-8'), sdl_color)
            if not surface:
                return 0
            w, h = surface.contents.w, surface.contents.h
            texture = SDL_CreateTextureFromSurface(self.renderer, surface)
            SDL_FreeSurface(surface)
            self.text_cache[key] = (texture, w, h)
        
        tex, w, h = self.text_cache[key]
        if tex:
            SDL_RenderCopy(self.renderer, tex, None, SDL_Rect(int(x), int(y), w, h))
        return w
    
    # === Render ===
    def render(self):
        self.draw_rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, Colors.BG_PRIMARY)
        self.render_header()
        
        if self.search_active:
            self.render_keyboard()
        else:
            self.render_content()
        
        self.render_navigation()
        SDL_RenderPresent(self.renderer)
        self.need_redraw = False
        self.frame_count += 1
    
    def draw_play_triangle(self, x, y, size, color):
        """Üçgen play butonu çiz"""
        # Üçgeni yatay çizgilerle doldur
        for i in range(size):
            # Üçgenin genişliği yukarıdan aşağıya artar sonra azalır
            half = size // 2
            if i <= half:
                width = (i * 2) // 3 + 1
            else:
                width = ((size - i) * 2) // 3 + 1
            
            start_x = x + (size - width) // 4
            self.draw_rect(start_x, y + i, width, 1, color)
    
    def measure_catalog_text(self, text, font):
        import ctypes
        if not font:
            return 0
        width, height = ctypes.c_int(), ctypes.c_int()
        ttf.TTF_SizeUTF8(font, str(text).encode("utf-8"), ctypes.byref(width), ctypes.byref(height))
        return width.value

    def fit_catalog_text(self, text, width, font):
        text = str(text or "").replace("\n", " ")
        if self.measure_catalog_text(text, font) <= width:
            return text
        while text and self.measure_catalog_text(text + "...", font) > width:
            text = text[:-1]
        return text.rstrip() + "..." if text else ""

    def draw_fitted_text(self, text, x, y, width, color, font):
        return self.draw_text(self.fit_catalog_text(text, width, font), x, y, color, font)

    def draw_centered_text(self, text, y, color, font, width):
        text = self.fit_catalog_text(text, width, font)
        x = (SCREEN_WIDTH - self.measure_catalog_text(text, font)) // 2
        return self.draw_text(text, x, y, color, font)

    def wrap_catalog_text(self, text, width, font, max_lines):
        words = str(text or "").split()
        result = []
        while words and len(result) < max_lines:
            if len(result) == max_lines - 1:
                result.append(self.fit_catalog_text(" ".join(words), width, font))
                break
            line = words.pop(0)
            while words and self.measure_catalog_text(line + " " + words[0], font) <= width:
                line += " " + words.pop(0)
            result.append(self.fit_catalog_text(line, width, font))
        return result

    def render_header(self):
        self.draw_rect(0, 0, SCREEN_WIDTH, 50, Colors.NAV_BG)
        # Film-strip mark, independent of any image library.
        self.draw_rect(16, 12, 28, 26, Colors.ACCENT)
        self.draw_rect(22, 16, 16, 18, Colors.NAV_BG)
        for yy in (15, 23, 31):
            self.draw_rect(18, yy, 2, 3, Colors.NAV_BG)
            self.draw_rect(40, yy, 2, 3, Colors.NAV_BG)
        self.draw_text("CINE", 55, 8, Colors.TEXT_PRIMARY, self.font_large)
        self.draw_text("R36S", 124, 18, Colors.MINT, self.font_small)
        self.draw_text("VIDEO LIBRARY", 466, 18, Colors.TEXT_SECONDARY, self.font_tiny)
        self.draw_rect(0, 49, SCREEN_WIDTH, 1, Colors.DIVIDER)

    
    def render_navigation(self):
        nav_y = SCREEN_HEIGHT - 55
        
        # Yardım metni - navbar üstünde
        help_y = nav_y - 18
        self.draw_rect(0, help_y, SCREEN_WIDTH, 18, Colors.BG_SECONDARY)
        
        # Klavye açıkken farklı yardım metni göster
        if self.search_active:
            help_text = self.t("help_keyboard")
        else:
            help_text = self.t("help_main")
        self.draw_text(help_text, SCREEN_WIDTH//2 - len(help_text)*3, help_y + 3, Colors.TEXT_TERTIARY, self.font_tiny)
        
        # Navigation bar
        self.draw_rect(0, nav_y, SCREEN_WIDTH, 55, Colors.NAV_BG)
        self.draw_rect(0, nav_y, SCREEN_WIDTH, 1, Colors.DIVIDER)
        
        items = [
            ("home", self.t("nav_home"), NAV_HOME),
            ("search", self.t("nav_search"), NAV_SEARCH),
            ("favorites", self.t("nav_favorites"), NAV_FAVORITES),
            ("history", self.t("nav_history"), NAV_HISTORY),
            ("settings", self.t("nav_settings"), NAV_SETTINGS)
        ]
        item_w = SCREEN_WIDTH // len(items)
        
        for i, (icon_type, label, nav_id) in enumerate(items):
            x = i * item_w
            cx = x + item_w // 2
            active = self.current_nav == nav_id
            
            # Active indicator
            if active:
                self.draw_rect(cx - 20, nav_y + 2, 40, 3, Colors.YT_RED)
            
            icon_color = Colors.NAV_ACTIVE if active else Colors.NAV_INACTIVE
            icon_y = nav_y + 12
            
            # İkonları çiz
            if icon_type == "home":
                # Ev ikonu - daha güzel versiyon
                # Çatı (üçgen)
                self.draw_rect(cx - 1, icon_y, 2, 2, icon_color)
                self.draw_rect(cx - 3, icon_y + 2, 6, 2, icon_color)
                self.draw_rect(cx - 5, icon_y + 4, 10, 2, icon_color)
                self.draw_rect(cx - 7, icon_y + 6, 14, 2, icon_color)
                # Gövde
                self.draw_rect(cx - 6, icon_y + 8, 12, 8, icon_color)
                # Kapı (boşluk)
                self.draw_rect(cx - 2, icon_y + 10, 4, 6, Colors.NAV_BG if active else Colors.BG_PRIMARY)
                # Baca
                self.draw_rect(cx + 3, icon_y - 1, 2, 4, icon_color)
            
            elif icon_type == "search":
                # Büyüteç ikonu - daha yuvarlak ve güzel
                # Daire (dış çerçeve)
                self.draw_rect(cx - 3, icon_y, 6, 2, icon_color)
                self.draw_rect(cx - 5, icon_y + 2, 2, 2, icon_color)
                self.draw_rect(cx + 3, icon_y + 2, 2, 2, icon_color)
                self.draw_rect(cx - 6, icon_y + 4, 2, 4, icon_color)
                self.draw_rect(cx + 4, icon_y + 4, 2, 4, icon_color)
                self.draw_rect(cx - 5, icon_y + 8, 2, 2, icon_color)
                self.draw_rect(cx + 3, icon_y + 8, 2, 2, icon_color)
                self.draw_rect(cx - 3, icon_y + 10, 6, 2, icon_color)
                # Sap (çapraz)
                self.draw_rect(cx + 4, icon_y + 11, 3, 2, icon_color)
                self.draw_rect(cx + 6, icon_y + 13, 3, 2, icon_color)
            
            elif icon_type == "favorites":
                # Kalp ikonu - favoriler için
                # Kalp üst kısmı (iki yarım daire)
                self.draw_rect(cx - 5, icon_y + 2, 4, 4, icon_color)
                self.draw_rect(cx + 1, icon_y + 2, 4, 4, icon_color)
                self.draw_rect(cx - 6, icon_y + 3, 2, 3, icon_color)
                self.draw_rect(cx + 4, icon_y + 3, 2, 3, icon_color)
                self.draw_rect(cx - 4, icon_y + 1, 2, 2, icon_color)
                self.draw_rect(cx + 2, icon_y + 1, 2, 2, icon_color)
                # Kalp alt kısmı (üçgen)
                self.draw_rect(cx - 6, icon_y + 5, 12, 3, icon_color)
                self.draw_rect(cx - 5, icon_y + 8, 10, 2, icon_color)
                self.draw_rect(cx - 4, icon_y + 10, 8, 2, icon_color)
                self.draw_rect(cx - 3, icon_y + 12, 6, 1, icon_color)
                self.draw_rect(cx - 2, icon_y + 13, 4, 1, icon_color)
                self.draw_rect(cx - 1, icon_y + 14, 2, 1, icon_color)
            
            elif icon_type == "history":
                # Saat ikonu - daha yuvarlak ve detaylı
                # Dış daire
                self.draw_rect(cx - 3, icon_y, 6, 2, icon_color)
                self.draw_rect(cx - 5, icon_y + 2, 2, 2, icon_color)
                self.draw_rect(cx + 3, icon_y + 2, 2, 2, icon_color)
                self.draw_rect(cx - 6, icon_y + 4, 2, 6, icon_color)
                self.draw_rect(cx + 4, icon_y + 4, 2, 6, icon_color)
                self.draw_rect(cx - 5, icon_y + 10, 2, 2, icon_color)
                self.draw_rect(cx + 3, icon_y + 10, 2, 2, icon_color)
                self.draw_rect(cx - 3, icon_y + 12, 6, 2, icon_color)
                # Merkez nokta
                self.draw_rect(cx - 1, icon_y + 6, 2, 2, icon_color)
                # Akrep (yukarı)
                self.draw_rect(cx - 1, icon_y + 3, 2, 3, icon_color)
                # Yelkovan (sağa)
                self.draw_rect(cx + 1, icon_y + 6, 3, 2, icon_color)
                # Geri ok işareti (sol tarafta)
                self.draw_rect(cx - 8, icon_y + 5, 2, 4, icon_color)
                self.draw_rect(cx - 10, icon_y + 7, 2, 2, icon_color)
                self.draw_rect(cx - 8, icon_y + 9, 2, 2, icon_color)
            
            elif icon_type == "settings":
                # Dişli ikonu - daha detaylı ve güzel
                # Merkez daire daire (iç boşluk)
                self.draw_rect(cx - 3, icon_y + 4, 6, 6, icon_color)
                # İç boşluk (daire efekti için)
                self.draw_rect(cx - 1, icon_y + 6, 2, 2, Colors.NAV_BG if active else Colors.BG_PRIMARY)
                # Üst diş
                self.draw_rect(cx - 2, icon_y, 4, 4, icon_color)
                # Alt diş
                self.draw_rect(cx - 2, icon_y + 10, 4, 4, icon_color)
                # Sol diş
                self.draw_rect(cx - 7, icon_y + 5, 4, 4, icon_color)
                # Sağ diş
                self.draw_rect(cx + 3, icon_y + 5, 4, 4, icon_color)
                # Sol üst çapraz diş
                self.draw_rect(cx - 6, icon_y + 1, 3, 3, icon_color)
                # Sağ üst çapraz diş
                self.draw_rect(cx + 3, icon_y + 1, 3, 3, icon_color)
                # Sol alt çapraz diş
                self.draw_rect(cx - 6, icon_y + 10, 3, 3, icon_color)
                # Sağ alt çapraz diş
                self.draw_rect(cx + 3, icon_y + 10, 3, 3, icon_color)
            
            # Label
            label_color = Colors.TEXT_PRIMARY if active else Colors.TEXT_TERTIARY
            self.draw_text(label, cx - len(label)*3, nav_y + 35, label_color, self.font_tiny)
    
    def render_content(self):
        y = 55
        h = SCREEN_HEIGHT - 55 - 73  # Header + nav + help text
        
        if self.current_nav == NAV_SETTINGS:
            self.render_settings(y, h)
            return
        
        # Arama yapılıyorsa searching ekranı göster
        if self.is_searching:
            self.render_searching(y)
            return
        
        videos = self._get_list()
        if videos:
            self.render_video_list(videos, y, h)
        else:
            self.render_empty(y)
    
    def render_searching(self, y):
        """Arama yapılırken gösterilecek ekran"""
        # Searching video yazısı
        msg = self.t("msg_searching")
        self.draw_text(msg, SCREEN_WIDTH//2 - len(msg)*5, y + 100, Colors.TEXT_SECONDARY, self.font)
        
        # Arama terimi
        if hasattr(self, 'last_search_query') and self.last_search_query:
            query_text = f'"{self.last_search_query}"'
            if len(query_text) > 35:
                query_text = query_text[:32] + '..."'
            self.draw_text(query_text, SCREEN_WIDTH//2 - len(query_text)*4, y + 130, Colors.TEXT_TERTIARY, self.font_small)
        
        # Loading spinner
        self.draw_spinner(SCREEN_WIDTH // 2, y + 190, radius=14, dot_size=4)
    
    def render_empty(self, y):
        msg = self.t("msg_press_search")
        if not self.ytdlp_path:
            msg = self.t("msg_no_ytdlp")
        elif not self.video_player:
            msg = self.t("msg_no_player")
        
        self.draw_text(msg, SCREEN_WIDTH//2 - len(msg)*5, y + 100, Colors.TEXT_SECONDARY, self.font)
        
        if not self.ytdlp_path:
            self.draw_text(self.t("msg_install_ytdlp"), 150, y + 140, Colors.TEXT_TERTIARY, self.font_tiny)
        if not self.video_player:
            self.draw_text(self.t("msg_install_player"), 170, y + 160, Colors.TEXT_TERTIARY, self.font_tiny)
        
        # Home sayfasında yükleme devam ediyorsa loading göster
        if self.current_nav == NAV_HOME and (self.is_loading or self.home_batch_loading):
            self.draw_spinner(SCREEN_WIDTH // 2, y + 200, radius=12, dot_size=3)
            self.draw_text(self.t("msg_loading_videos"), SCREEN_WIDTH // 2 - 55, y + 230, Colors.TEXT_TERTIARY, self.font_small)
    
    def render_settings(self, start_y, height):
        # Title ve Cine R36s branding - aynı satırda
        self.draw_text(self.t("settings_title"), 20, start_y + 10, Colors.TEXT_PRIMARY, self.font_large)
        
        # Cine R36s yazısı - sağ üst köşede, Settings ile aynı hizada
        brand_x = SCREEN_WIDTH - 105
        brand_y = start_y + 12
        self.draw_text("Cine R36s", brand_x, brand_y, Colors.TEXT_PRIMARY, self.font_small)
        
        item_h = 50
        margin = 5
        list_start_y = start_y + 50
        list_height = height - 60  # Alt kısım için boşluk bırak
        visible_count = list_height // (item_h + margin)
        
        # Scroll kontrolü
        if self.settings_selected < self.settings_scroll:
            self.settings_scroll = self.settings_selected
        elif self.settings_selected >= self.settings_scroll + visible_count:
            self.settings_scroll = self.settings_selected - visible_count + 1
        
        # Görünür öğeleri çiz
        y = list_start_y
        for i in range(self.settings_scroll, min(self.settings_scroll + visible_count, len(self.settings_items))):
            label, key, options = self.settings_items[i]
            selected = i == self.settings_selected
            
            # Background
            if selected:
                self.draw_rect(15, y, SCREEN_WIDTH - 30, item_h, Colors.CARD_SELECTED)
                self.draw_rect(15, y, 4, item_h, Colors.YT_RED)
            else:
                self.draw_rect(15, y, SCREEN_WIDTH - 30, item_h, Colors.CARD_BG)
            
            # Label
            self.draw_text(label, 30, y + 15, Colors.TEXT_PRIMARY if selected else Colors.TEXT_SECONDARY, self.font)
            
            # Value or action
            if options is None:
                # Action button
                self.draw_text(self.t("settings_execute"), SCREEN_WIDTH - 130, y + 15, Colors.YT_RED, self.font_small)
            else:
                # Current value with arrows
                current = self.settings.get(key, options[0])
                if key == "full_screen":
                    current = self.t("settings_on") if current == "On" else self.t("settings_off")
                self.draw_text(f"< {current} >", SCREEN_WIDTH - 130, y + 15, Colors.TEXT_PRIMARY if selected else Colors.TEXT_TERTIARY, self.font)
            
            y += item_h + margin
        
        # Scrollbar (eğer gerekiyorsa)
        if len(self.settings_items) > visible_count:
            sb_height = list_height
            thumb_height = max(20, int(sb_height * visible_count / len(self.settings_items)))
            thumb_y = list_start_y + int((sb_height - thumb_height) * self.settings_scroll / max(1, len(self.settings_items) - visible_count))
            self.draw_rect(SCREEN_WIDTH - 8, list_start_y, 4, sb_height, Colors.PROGRESS_BG)
            self.draw_rect(SCREEN_WIDTH - 8, thumb_y, 4, thumb_height, Colors.YT_RED)
    
    def change_setting(self, direction):
        """Ayar değerini değiştir (sadece seçenekli ayarlar için)"""
        if self.settings_selected >= len(self.settings_items):
            return
        
        label, key, options = self.settings_items[self.settings_selected]
        
        if options is None:
            # Action item - left/right ile değiştirilemez, sadece A tuşu ile çalışır
            # Bu fonksiyon hiçbir şey yapmamalı
            return
        
        current = self.settings.get(key, options[0])
        if key == "full_screen":
            options = ["On", "Off"]
        try:
            idx = options.index(current)
        except:
            idx = 0
        
        if direction > 0:
            idx = (idx + 1) % len(options)
        else:
            idx = (idx - 1) % len(options)
        
        self.settings[key] = options[idx]
        self._save_settings()
        
        # Dil değiştiğinde settings items'ı ve text cache'i güncelle
        if key == "language":
            self._update_settings_items()
            self.text_cache.clear()
        
        value_label = self.t("settings_on") if options[idx] == "On" else self.t("settings_off")
        self.status = f"{label}: {value_label if key == 'full_screen' else options[idx]}"
        self.status_type = "ok"
        self.need_redraw = True
    
    def execute_setting_action(self, key):
        """Ayar aksiyonunu çalıştır"""
        if key == "clear_favorites":
            self.favorites = []
            self._save_json("yt_favorites.json", [])
            self.status = self.t("msg_fav_cleared")
            self.status_type = "ok"
        elif key == "clear_history":
            self.history = []
            self._save_json("yt_history.json", [])
            self.status = self.t("msg_history_cleared")
            self.status_type = "ok"
        elif key == "clear_cache":
            try:
                import shutil
                if os.path.exists(self.image_cache_dir):
                    shutil.rmtree(self.image_cache_dir)
                    os.makedirs(self.image_cache_dir, exist_ok=True)
                self.image_cache.clear()
                self.failed_images.clear()
                self.status = self.t("msg_cache_cleared")
                self.status_type = "ok"
            except Exception as e:
                self.status = f"Error: {str(e)[:20]}"
                self.status_type = "error"
        self.need_redraw = True
    
    def render_video_list(self, videos, start_y, height):
        if not videos:
            return
        self.selected = max(0, min(self.selected, len(videos) - 1))
        video = videos[self.selected]
        labels = {NAV_HOME: self.t("nav_home"), NAV_SEARCH: self.t("nav_search"),
                  NAV_FAVORITES: self.t("nav_favorites"), NAV_HISTORY: self.t("nav_history")}
        label = labels.get(self.current_nav, "Library")
        if self.current_nav == NAV_SEARCH and self.last_search_query:
            label += " / " + self.last_search_query
        self.draw_fitted_text(label, 16, start_y + 2, 470, Colors.MINT, self.font_small)
        self.draw_text("%d / %d" % (self.selected + 1, len(videos)), 548, start_y + 2,
                       Colors.TEXT_SECONDARY, self.font_small)

        # Keep original thumbnails at their actual aspect ratio; no fake posters or ratings.
        preview_y = start_y + 29
        self.draw_thumbnail(16, preview_y, 320, 180, video.thumbnail)
        info_x = 352
        title_lines = self.wrap_catalog_text(video.title, 267, self.font, 3)
        for i, line in enumerate(title_lines):
            self.draw_text(line, info_x, preview_y + 7 + i * 23, Colors.TEXT_PRIMARY, self.font)
        self.draw_fitted_text(video.channel, info_x, preview_y + 88, 265,
                              Colors.MINT, self.font_small)
        meta = " / ".join(filter(None, [video.format_duration(), video.format_views(), video.format_date()]))
        self.draw_fitted_text(meta, info_x, preview_y + 112, 265, Colors.TEXT_SECONDARY, self.font_tiny)
        self.draw_rect(info_x, preview_y + 149, 28, 25, Colors.ACCENT)
        self.draw_play_triangle(info_x + 9, preview_y + 155, 12, Colors.BG_PRIMARY)
        self.draw_text("[A]", info_x + 39, preview_y + 153, Colors.TEXT_PRIMARY, self.font_small)
        if any(v.id == video.id for v in self.favorites):
            self.draw_text("*", 598, preview_y + 151, Colors.MINT, self.font)

        # Poster shelf: 6 capas lado a lado, esquerda/direita troca de filme
        per = 6
        self.scroll = (self.selected // per) * per
        shelf_y = preview_y + 188
        cw, ch = 96, 72
        for col, item in enumerate(videos[self.scroll:self.scroll + per]):
            x = 16 + col * 102
            active = self.scroll + col == self.selected
            self.draw_rect(x, shelf_y, cw, ch + 30, Colors.CARD_SELECTED if active else Colors.CARD_BG)
            self.draw_thumbnail(x + 2, shelf_y + 2, cw - 4, ch, item.thumbnail)
            self.draw_fitted_text(item.title, x + 3, shelf_y + ch + 8, cw - 6,
                                  Colors.TEXT_PRIMARY if active else Colors.TEXT_SECONDARY, self.font_tiny)
            if active:
                self.draw_rect(x, shelf_y + ch + 27, cw, 3, Colors.ACCENT)
        # pre-carrega capas da proxima pagina
        for item in videos[self.scroll + per:self.scroll + per * 2]:
            if item.thumbnail and item.thumbnail not in self.image_cache:
                self.load_thumbnail(item.thumbnail)
        batch_loading = ((self.current_nav == NAV_HOME and self.home_batch_loading) or
                         (self.current_nav == NAV_SEARCH and self.search_batch_loading))
        self.loading_spinner_triggered = batch_loading and self.selected >= len(videos) - 3
        if self.loading_spinner_triggered:
            self.draw_spinner(529, start_y + 11, radius=7, dot_size=2)

    
    def render_keyboard(self):
        kb_y = SCREEN_HEIGHT - 260
        self.draw_rect(0, kb_y - 45, SCREEN_WIDTH, SCREEN_HEIGHT - kb_y + 45, (0, 0, 0), 240)
        
        # Input
        input_y = kb_y - 38
        self.draw_rect(15, input_y, SCREEN_WIDTH - 30, 32, Colors.BG_TERTIARY)
        self.draw_rect(15, input_y, SCREEN_WIDTH - 30, 2, Colors.YT_RED)
        
        query = self.search_query or self.t("kb_search_placeholder")
        color = Colors.TEXT_PRIMARY if self.search_query else Colors.TEXT_TERTIARY
        
        # Yazıyı çiz ve gerçek genişliği al
        display_query = query[:35]
        text_width = self.draw_text(display_query, 25, input_y + 7, color, self.font)
        
        # Cursor - gerçek metin genişliğine göre konumlandır
        if self.search_query and (self.frame_count // 15) % 2:
            cursor_x = 25 + text_width + 2
            self.draw_rect(cursor_x, input_y + 5, 2, 20, Colors.YT_RED)
        
        # Keys
        key_w, key_h, gap = 52, 34, 4
        offsets = [15, 15, 35, 55]  # Rakamlar, qwerty, asdf, zxcv
        
        layout = self.keyboard_layout.copy()
        if self.caps_lock:
            # Sadece harfleri büyüt (satır 1, 2, 3 - rakamlar satır 0)
            layout = [layout[0]] + [[c.upper() for c in row] for row in layout[1:4]]
        
        for row_i, row in enumerate(layout):
            for col_i, char in enumerate(row):
                x = offsets[row_i] + col_i * (key_w + gap)
                y = kb_y + row_i * (key_h + gap)
                selected = self.keyboard_row == row_i and self.keyboard_col == col_i
                
                self.draw_rect(x, y, key_w, key_h, Colors.YT_RED if selected else Colors.BG_TERTIARY)
                self.draw_text(char, x + key_w//2 - 5, y + 7, Colors.TEXT_PRIMARY, self.font)
        
        # Controls
        ctrl_y = kb_y + 4 * (key_h + gap)
        ctrls = [("ABC" if self.caps_lock else "abc", 55), (self.t("kb_space"), 180), ("<-", 55), (self.t("kb_go"), 80)]
        ctrl_x = 15
        
        for i, (label, w) in enumerate(ctrls):
            selected = self.keyboard_row == 4 and self.keyboard_col == i
            bg = Colors.YT_RED if (selected or (i == 3)) else Colors.BG_TERTIARY
            self.draw_rect(ctrl_x, ctrl_y, w, key_h, bg if not selected else Colors.YT_RED)
            self.draw_text(label, ctrl_x + w//2 - len(label)*4, ctrl_y + 7, Colors.TEXT_PRIMARY, self.font_small)
            ctrl_x += w + gap
        
        self.draw_text(self.t("help_keyboard"), 140, ctrl_y + key_h + 8, Colors.TEXT_TERTIARY, self.font_tiny)
    
    # === Input ===
    def _get_list(self):
        if self.current_nav == NAV_HOME:
            return self.home_videos
        if self.current_nav == NAV_SEARCH:
            return self.search_results
        if self.current_nav == NAV_FAVORITES:
            return self.favorites
        if self.current_nav == NAV_HISTORY:
            return self.history
        return []
    
    def handle_keyboard_nav(self, d):
        lens = [10, 10, 9, 7, 4]  # 1234567890, qwertyuiop, asdfghjkl, zxcvbnm, controls
        if d == "up" and self.keyboard_row > 0:
            self.keyboard_row -= 1
            self.keyboard_col = min(self.keyboard_col, lens[self.keyboard_row] - 1)
        elif d == "down" and self.keyboard_row < 4:
            self.keyboard_row += 1
            self.keyboard_col = min(self.keyboard_col, lens[self.keyboard_row] - 1)
        elif d == "left" and self.keyboard_col > 0:
            self.keyboard_col -= 1
        elif d == "right" and self.keyboard_col < lens[self.keyboard_row] - 1:
            self.keyboard_col += 1
        self.need_redraw = True
    
    def handle_keyboard_select(self):
        if self.keyboard_row < 4:
            layout = self.keyboard_layout.copy()
            if self.caps_lock:
                # Sadece harfleri büyüt (satır 1, 2, 3 - rakamlar satır 0)
                layout = [layout[0]] + [[c.upper() for c in row] for row in layout[1:4]]
            row = layout[self.keyboard_row]
            if self.keyboard_col < len(row) and len(self.search_query) < 50:
                self.search_query += row[self.keyboard_col]
        else:
            if self.keyboard_col == 0:
                self.caps_lock = not self.caps_lock
            elif self.keyboard_col == 1 and len(self.search_query) < 50:
                self.search_query += " "
            elif self.keyboard_col == 2 and self.search_query:
                self.search_query = self.search_query[:-1]
            elif self.keyboard_col == 3 and self.search_query.strip():
                self.search_youtube(self.search_query.strip())
        self.need_redraw = True
    
    def action_up(self):
        if self.selected > 0:
            self.selected -= 1
            self.need_redraw = True
    
    def action_down(self):
        videos = self._get_list()
        if self.selected < len(videos) - 1:
            self.selected += 1
            self.need_redraw = True
            # Sonraki batch'i yükle gerekiyorsa
            self.check_load_next_batch()
    
    def _in_movie_list(self):
        return (not self.search_active and self.current_nav != NAV_SETTINGS
                and len(self._get_list()) > 0)

    def move_left(self):
        if self._in_movie_list():
            self.action_up()
        else:
            self.action_left()

    def move_right(self):
        if self._in_movie_list():
            self.action_down()
        else:
            self.action_right()

    def action_left(self):
        self.current_nav = (self.current_nav - 1) % 5
        self.selected = self.scroll = 0
        self.loading_spinner_triggered = False
        self.need_redraw = True
    
    def action_right(self):
        self.current_nav = (self.current_nav + 1) % 5
        self.selected = self.scroll = 0
        self.loading_spinner_triggered = False
        self.need_redraw = True
    
    def action_select(self):
        if self.current_nav == NAV_SEARCH and not self.search_results:
            self.search_active = True
            self.search_query = ""
            self.keyboard_row = self.keyboard_col = 0
        else:
            videos = self._get_list()
            if videos and self.selected < len(videos):
                self.play_video(videos[self.selected])
        self.need_redraw = True
    
    def action_back(self):
        if self.search_active:
            self.search_active = False
        elif self.is_playing:
            self.stop_playback()
        else:
            self.running = False
        self.need_redraw = True
    
    def action_search(self):
        self.search_active = True
        self.search_query = ""
        self.keyboard_row = self.keyboard_col = 0
        self.current_nav = NAV_SEARCH
        self.need_redraw = True
    
    def toggle_favorite(self):
        """Seçili videoyu favorilere ekle veya çıkar"""
        videos = self._get_list()
        if not videos or self.selected >= len(videos):
            return
        
        video = videos[self.selected]
        
        # Favori listesinde var mı kontrol et
        is_favorite = any(v.id == video.id for v in self.favorites)
        
        if is_favorite:
            # Favorilerden çıkar
            self.favorites = [v for v in self.favorites if v.id != video.id]
            self.status = self.t("msg_removed_fav")
        else:
            # Favorilere ekle
            self.favorites.insert(0, video)
            self.status = self.t("msg_added_fav")
        
        self._save_json("yt_favorites.json", self.favorites)
        self.status_type = "ok"
        self.need_redraw = True
    
    def process_repeat(self):
        if not self.key_held:
            return
        now = SDL_GetTicks()
        if now - self.key_hold_start < 400:
            return
        if now - self.last_repeat >= 100:
            self.last_repeat = now
            if self.search_active:
                self.handle_keyboard_nav(self.key_held)
            elif self.key_held == "up":
                self.action_up()
            elif self.key_held == "down":
                self.action_down()
    
    def handle_event(self, event):
        now = SDL_GetTicks()
        
        # Video yüklenirken tüm input'ları devre dışı bırak
        if self.is_loading_video:
            return
        
        if self.search_active:
            if event.type == SDL_CONTROLLERBUTTONDOWN:
                btn = event.cbutton.button
                if btn == SDL_CONTROLLER_BUTTON_DPAD_UP:
                    self.handle_keyboard_nav("up")
                    self.key_held, self.key_hold_start = "up", now
                elif btn == SDL_CONTROLLER_BUTTON_DPAD_DOWN:
                    self.handle_keyboard_nav("down")
                    self.key_held, self.key_hold_start = "down", now
                elif btn == SDL_CONTROLLER_BUTTON_DPAD_LEFT:
                    self.handle_keyboard_nav("left")
                elif btn == SDL_CONTROLLER_BUTTON_DPAD_RIGHT:
                    self.handle_keyboard_nav("right")
                elif btn == SDL_CONTROLLER_BUTTON_A:
                    self.handle_keyboard_select()
                elif btn == SDL_CONTROLLER_BUTTON_B:
                    self.search_active = False
                    self.need_redraw = True
                elif btn == SDL_CONTROLLER_BUTTON_START:
                    if self.search_query.strip():
                        self.search_youtube(self.search_query.strip())
                elif btn == SDL_CONTROLLER_BUTTON_Y:
                    if self.search_query:
                        self.search_query = self.search_query[:-1]
                        self.need_redraw = True
            elif event.type == SDL_CONTROLLERBUTTONUP:
                self.key_held = None
            elif event.type == SDL_JOYHATMOTION:
                hat = event.jhat.value
                if hat & SDL_HAT_UP:
                    self.handle_keyboard_nav("up")
                    self.key_held, self.key_hold_start = "up", now
                elif hat & SDL_HAT_DOWN:
                    self.handle_keyboard_nav("down")
                    self.key_held, self.key_hold_start = "down", now
                elif hat & SDL_HAT_LEFT:
                    self.handle_keyboard_nav("left")
                elif hat & SDL_HAT_RIGHT:
                    self.handle_keyboard_nav("right")
                else:
                    self.key_held = None
            return
        
        if event.type == SDL_CONTROLLERBUTTONDOWN:
            btn = event.cbutton.button
            
            # Video oynatılırken kontroller
            if self.is_playing:
                if btn == SDL_CONTROLLER_BUTTON_B:
                    self.stop_playback()
                elif btn == SDL_CONTROLLER_BUTTON_Y:
                    self.player_toggle_pause()
                elif btn == SDL_CONTROLLER_BUTTON_LEFTSHOULDER:
                    self.player_seek(-10)  # 10 saniye geri
                elif btn == SDL_CONTROLLER_BUTTON_RIGHTSHOULDER:
                    self.player_seek(10)   # 10 saniye ileri
                elif btn == SDL_CONTROLLER_BUTTON_DPAD_LEFT:
                    self.player_seek(-5)   # 5 saniye geri
                elif btn == SDL_CONTROLLER_BUTTON_DPAD_RIGHT:
                    self.player_seek(5)    # 5 saniye ileri
                elif btn == SDL_CONTROLLER_BUTTON_DPAD_UP:
                    self.player_brightness(5)  # Parlaklık artır
                elif btn == SDL_CONTROLLER_BUTTON_DPAD_DOWN:
                    self.player_brightness(-5)  # Parlaklık azalt
                return
            
            # Settings sayfasında kontroller
            if self.current_nav == NAV_SETTINGS:
                if btn == SDL_CONTROLLER_BUTTON_A:
                    # A tuşu ile seçili ayarı değiştir veya aksiyonu çalıştır
                    label, key, options = self.settings_items[self.settings_selected]
                    if options is None:
                        # Action item - çalıştır
                        self.execute_setting_action(key)
                    else:
                        # Seçenekli ayar - değeri değiştir
                        self.change_setting(1)
                elif btn == SDL_CONTROLLER_BUTTON_B:
                    self.action_back()
                elif btn == SDL_CONTROLLER_BUTTON_DPAD_UP:
                    if self.settings_selected > 0:
                        self.settings_selected -= 1
                        self.need_redraw = True
                elif btn == SDL_CONTROLLER_BUTTON_DPAD_DOWN:
                    if self.settings_selected < len(self.settings_items) - 1:
                        self.settings_selected += 1
                        self.need_redraw = True
                elif btn == SDL_CONTROLLER_BUTTON_DPAD_LEFT:
                    # Action item'da (options=None) sekme değiştir, değilse ayarı değiştir
                    _, _, options = self.settings_items[self.settings_selected]
                    if options is None:
                        self.action_left()
                    else:
                        self.change_setting(-1)
                elif btn == SDL_CONTROLLER_BUTTON_DPAD_RIGHT:
                    # Action item'da (options=None) sekme değiştir, değilse ayarı değiştir
                    _, _, options = self.settings_items[self.settings_selected]
                    if options is None:
                        self.action_right()
                    else:
                        self.change_setting(1)
                elif btn == SDL_CONTROLLER_BUTTON_LEFTSHOULDER:
                    self.action_left()
                elif btn == SDL_CONTROLLER_BUTTON_RIGHTSHOULDER:
                    self.action_right()
                return
            
            if btn == SDL_CONTROLLER_BUTTON_A:
                self.action_select()
            elif btn == SDL_CONTROLLER_BUTTON_B:
                self.action_back()
            elif btn == SDL_CONTROLLER_BUTTON_X:
                self.action_search()
            elif btn == SDL_CONTROLLER_BUTTON_Y:
                self.toggle_favorite()  # Y tuşu ile favorilere ekle/çıkar
            elif btn == SDL_CONTROLLER_BUTTON_DPAD_UP:
                self.action_up()
                self.key_held, self.key_hold_start = "up", now
            elif btn == SDL_CONTROLLER_BUTTON_DPAD_DOWN:
                self.action_down()
                self.key_held, self.key_hold_start = "down", now
            elif btn == SDL_CONTROLLER_BUTTON_DPAD_LEFT:
                self.move_left()
            elif btn == SDL_CONTROLLER_BUTTON_DPAD_RIGHT:
                self.move_right()
            elif btn in (SDL_CONTROLLER_BUTTON_LEFTSHOULDER, SDL_CONTROLLER_BUTTON_RIGHTSHOULDER):
                if btn == SDL_CONTROLLER_BUTTON_LEFTSHOULDER:
                    self.action_left()
                else:
                    self.action_right()
            elif btn == SDL_CONTROLLER_BUTTON_START:
                self.action_search()
        elif event.type == SDL_CONTROLLERBUTTONUP:
            self.key_held = None
        elif event.type == SDL_JOYHATMOTION:
            hat = event.jhat.value
            
            # Video oynatılırken kontroller
            if self.is_playing:
                if hat & SDL_HAT_LEFT:
                    self.player_seek(-5)
                elif hat & SDL_HAT_RIGHT:
                    self.player_seek(5)
                elif hat & SDL_HAT_UP:
                    self.player_brightness(5)
                elif hat & SDL_HAT_DOWN:
                    self.player_brightness(-5)
                return
            
            # Settings sayfasında
            if self.current_nav == NAV_SETTINGS:
                if hat & SDL_HAT_UP:
                    if self.settings_selected > 0:
                        self.settings_selected -= 1
                        self.need_redraw = True
                elif hat & SDL_HAT_DOWN:
                    if self.settings_selected < len(self.settings_items) - 1:
                        self.settings_selected += 1
                        self.need_redraw = True
                elif hat & SDL_HAT_LEFT:
                    # Action item'da (options=None) sekme değiştir, değilse ayarı değiştir
                    _, _, options = self.settings_items[self.settings_selected]
                    if options is None:
                        self.action_left()
                    else:
                        self.change_setting(-1)
                elif hat & SDL_HAT_RIGHT:
                    # Action item'da (options=None) sekme değiştir, değilse ayarı değiştir
                    _, _, options = self.settings_items[self.settings_selected]
                    if options is None:
                        self.action_right()
                    else:
                        self.change_setting(1)
                else:
                    self.key_held = None
                return
            
            if hat & SDL_HAT_UP:
                self.action_up()
                self.key_held, self.key_hold_start = "up", now
            elif hat & SDL_HAT_DOWN:
                self.action_down()
                self.key_held, self.key_hold_start = "down", now
            elif hat & SDL_HAT_LEFT:
                self.move_left()
            elif hat & SDL_HAT_RIGHT:
                self.move_right()
            else:
                self.key_held = None
        elif event.type == SDL_KEYDOWN:
            key = event.key.keysym.sym
            if key in (SDLK_UP, SDLK_w):
                self.action_up()
            elif key in (SDLK_DOWN, SDLK_s):
                self.action_down()
            elif key in (SDLK_LEFT, SDLK_a):
                self.move_left()
            elif key in (SDLK_RIGHT, SDLK_d):
                self.move_right()
            elif key == SDLK_q:
                self.action_left()
            elif key == SDLK_e:
                self.action_right()
            elif key in (SDLK_RETURN, SDLK_z):
                self.action_select()
            elif key in (SDLK_ESCAPE, SDLK_x):
                self.action_back()
    
    def run(self):
        if self.ytdlp_path:
            self.load_trending()
        
        event = SDL_Event()
        last_render_time = 0
        while self.running:
            while SDL_PollEvent(event):
                if event.type == SDL_QUIT:
                    self.running = False
                else:
                    self.handle_event(event)
            
            self.process_repeat()
            
            current_time = SDL_GetTicks()
            
            # Video yüklenirken loading ekranı göster
            if self.is_loading_video:
                self.render_loading_screen(self.t("msg_loading_video"), self.current_video.title if self.current_video else "")
            # Video oynatılırken render yapma (pencere zaten gizli)
            elif not self.is_playing:
                # Batch loading veya arama sırasında da render yap (spinner animasyonu için)
                is_batch_loading = self.home_batch_loading or self.search_batch_loading
                # Her 100ms'de bir zorunlu render yap (thread'den gelen değişiklikleri yakalamak için)
                force_render = (current_time - last_render_time) >= 100
                if self.need_redraw or self.is_loading or self.loading_images or is_batch_loading or self.is_searching or force_render:
                    self.render()
                    last_render_time = current_time
            
            SDL_Delay(16)
        
        self.cleanup()
    
    def cleanup(self):
        self.stop_playback()
        
        for tex, _, _ in self.text_cache.values():
            if tex:
                SDL_DestroyTexture(tex)
        for tex, _, _ in self.image_cache.values():
            if tex:
                SDL_DestroyTexture(tex)
        
        if self.font:
            ttf.TTF_CloseFont(self.font)
        if self.font_large:
            ttf.TTF_CloseFont(self.font_large)
        if self.font_small:
            ttf.TTF_CloseFont(self.font_small)
        if self.font_tiny:
            ttf.TTF_CloseFont(self.font_tiny)
        
        if self.controller:
            SDL_GameControllerClose(self.controller)
        if self.joystick:
            SDL_JoystickClose(self.joystick)
        
        ttf.TTF_Quit()
        SDL_DestroyRenderer(self.renderer)
        SDL_DestroyWindow(self.window)
        SDL_Quit()


if __name__ == "__main__":
    print(f"Script dir: {SCRIPT_DIR}")
    print(f"yt-dlp: {YTDLP_PATH}")
    print(f"Player: {VIDEO_PLAYER}")
    
    try:
        app = CineApp()
        app.run()
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
