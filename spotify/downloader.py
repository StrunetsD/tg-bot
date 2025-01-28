import asyncio
import json
from datetime import datetime
from pathlib import Path

from asyncer import asyncify
from spotdl import Song
from spotdl.download.downloader import Downloader as BaseDownloader
from spotdl.download.downloader import logger
from spotdl.utils.m3u import gen_m3u_files
from spotdl.utils.search import songs_from_albums


class Downloader(BaseDownloader):
    async def download_song(self, song: Song):
        self.progress_handler.set_song_count(1)
        return (await self.download_multiple_songs([song]))[0]

    async def download_multiple_songs(self, songs):
        if self.settings['fetch_albums']:
            raw_albums: list[str] = [
                song.album_id for song in songs if song.album_id is not None
            ]
            albums: set[str] = set(raw_albums)

            logger.info(
                'Fetching %d album%s', len(albums), 's' if len(albums) > 1 else ''
            )

            songs.extend(songs_from_albums(list(albums)))
            songs = list({song.url: song for song in songs}.values())

        logger.debug('Downloading %d songs', len(songs))

        if self.settings['archive']:
            songs = [song for song in songs if song.url not in self.url_archive]
            logger.debug('Filtered %d songs with archive', len(songs))

        self.progress_handler.set_song_count(len(songs))

        results: list[tuple[Song, Path | None]] = await asyncio.gather(
            *[asyncify(self.search_and_download)(song) for song in songs]
        )

        if self.settings['print_errors']:
            for error in self.errors:
                logger.error(error)

        if self.settings['save_errors']:
            with open(self.settings['save_errors'], 'a') as error_file:
                if len(self.errors) > 0:
                    error_file.write(
                        f'{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}\n'
                    )

                for error in self.errors:
                    error_file.write(f'{error}\n')

            logger.info('Saved errors to %s', self.settings['save_errors'])

        if self.settings['archive']:
            for result in results:
                if result[1] or self.settings['add_unavailable']:
                    self.url_archive.add(result[0].url)

            self.url_archive.save(self.settings['archive'])
            logger.info(
                'Saved archive with %d urls to %s',
                len(self.url_archive),
                self.settings['archive'],
            )

        if self.settings['m3u']:
            song_list = [
                song
                for song, path in results
                if path or self.settings['add_unavailable']
            ]

            gen_m3u_files(
                song_list,
                self.settings['m3u'],
                self.settings['output'],
                self.settings['format'],
                self.settings['restrict'],
                False,
                self.settings['detect_formats'],
            )

        if self.settings['save_file']:
            with open(self.settings['save_file'], 'w') as save_file:
                json.dump(
                    [song.json for song, path in results],
                    save_file,
                    indent=4,
                    ensure_ascii=False,
                )

            logger.info('Saved results to %s', self.settings['save_file'])

        return results
