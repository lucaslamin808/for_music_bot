from decouple import config

# TOKENS
BOT_TOKEN = config('TOKEN')
API_KEY = config('API_JSON')
GCS_ENGINE_ID = config('GOOGLE_ID')
SPOTIFY_ID = ""
SPOTIFY_SECRET = ""

# PREFIXO PARA USAR COMANDOS
BOT_PREFIX = "!"

# CORES (você pode mudá-las colocando o código decímal após o "0x")
EMBED_COLOR = 0x7DCE82 # ciano
EMBED_COLOR_OK = 0x9BE89B # verde
EMBED_COLOR_ERROR = 0xFF9494 # vermelho

MAX_SONG_PRELOAD = 20  # o máximo é 25
COOKIE_PATH = "/config/cookies/cookies.txt"
GLOBAL_DISABLE_AUTOJOIN_VC = False

VC_TIMEOUT = 5000 # segundos
VC_TIMOUT_DEFAULT = True  
ALLOW_VC_TIMEOUT_EDIT = True  

STARTUP_MESSAGE = "Iniciando..."
STARTUP_COMPLETE_MESSAGE = "Bot Online!"

# MENSAGENS DE ERRO
NO_GUILD_MESSAGE = 'Erro: Você deve estar em um canal de voz para usar essse comando!'
USER_NOT_IN_VC_MESSAGE = "Erro: Por fovor entre em um canal de voz para enviar comandos!"
WRONG_CHANNEL_MESSAGE = "Erro: Por favor use o canal de comandos para enviar comandos!"
NOT_CONNECTED_MESSAGE = "Erro: Não estOU conectado a nenhum canal de voz!"
ALREADY_CONNECTED_MESSAGE = "Erro: Já estou conectado ao canal de voz!"
CHANNEL_NOT_FOUND_MESSAGE = "Erro: Não consigo encontrar o canal!"
DEFAULT_CHANNEL_JOIN_FAILED = "Erro: Não consigo entrar no canal de voz padrão!"
SONGINFO_ERROR = "Erro: Link não suportado!"

INFO_HISTORY_TITLE = "Músicas reproduzidas:"
MAX_HISTORY_LENGTH = 10
MAX_TRACKNAME_HISTORY_LENGTH = 15

# MENSAGENS PARA REPRODUÇÃO
SONGINFO_UPLOADER = "Canal: "
SONGINFO_DURATION = "Duração: "
SONGINFO_SECONDS = "s"
SONGINFO_LIKES = "Likes: "
SONGINFO_DISLIKES = "Dislikes: "
SONGINFO_NOW_PLAYING = "Reproduzindo agora"
SONGINFO_QUEUE_ADDED = "Adicionado a fila"
SONGINFO_SONGINFO = "Song info"
SONGINFO_UNKNOWN_DURATION = "Desconhecido"
SONGINFO_PLAYLIST_QUEUED = "Playlist adicionada :page_with_curl:"

# MENSAGENS DE AJUDA
HELP_CONNECT = "Conecta o bot ao canal de voz."
HELP_DISCONNECT = "Desconecta o bot do canal de voz."
HELP_SETTINGS = "Ver e editar as configurações do bot."
HELP_HISTORY = "Mostra o histórico de músicas."
HELP_PAUSE = "Pausa a música."
HELP_VOL = "Altera o %volume."
HELP_PREV = "Reproduz a música anterior."
HELP_RESUME = "Volta a reproduzir a música pausada."
HELP_SKIP = "Pula uma música."
HELP_SONGINFO = "Exibe as informações da música."
HELP_LYRICS = "Exibe a letra da música."
HELP_STOP = "Cancela toda a fila de músicas."
HELP_YT = "Reproduz uma música."
HELP_PING = "Pong."
HELP_CLEAR = "Limpa a fila."
HELP_LOOP = "Loop da música atual on/off."
HELP_QUEUE = "Exibe as músicas na fila."
HELP_SHUFFLE = "Torna a fila aleatória."
HELP_CHANGECHANNEL = "Troca o bot de canal."
HELP_HELP = "Exibe essa mensagem."

ABSOLUTE_PATH = '' # não altere