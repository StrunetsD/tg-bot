import logging

from music_bot.bot.handlers import *
from music_bot.bot.tasks import run_tasks


async def main():
    await asyncio.gather(
        dp.start_polling(bot),
        run_tasks()
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
