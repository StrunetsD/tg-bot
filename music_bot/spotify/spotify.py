from dotenv import load_dotenv
from spotdl import DownloaderOptions, Song
from spotdl.utils.config import DOWNLOADER_OPTIONS
from spotdl.utils.search import parse_query
from spotdl.utils.spotify import SpotifyClient

from core.config import TRACKS_PATH
from .downloader import Downloader

load_dotenv()


class Spotify:
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            settings: DownloaderOptions | None = None,
    ):
        SpotifyClient.init(client_id=client_id, client_secret=client_secret)

        # обновление настроек загрузчика
        bundle_settings: DownloaderOptions = DOWNLOADER_OPTIONS.copy()

        if settings:
            bundle_settings.update(settings)

        bundle_settings['simple_tui'] = True
        bundle_settings['output'] = str(TRACKS_PATH)

        self.downloader = Downloader(settings=bundle_settings)

    async def search(self, query: list[str]) -> list[Song]:
        return parse_query(
            query=query,
            threads=self.downloader.settings['threads'],
            use_ytm_data=self.downloader.settings['ytm_data'],
            playlist_numbering=self.downloader.settings['playlist_numbering'],
            album_type=self.downloader.settings['album_type'],
            playlist_retain_track_cover=self.downloader.settings[
                'playlist_retain_track_cover'
            ],
        )

    async def download(self, song: Song):
        song, path = await self.downloader.download_song(song=song)
        assert path
        return song, path
