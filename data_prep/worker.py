import asyncio
import json
import os
import traceback
from urllib import error

import aiohttp
import click
from bs4 import BeautifulSoup

from db import CharacterModel, EpisodeModel, Session

simpsons_base_url = "https://simpsons.wikia.com"


def get_url(params, limit=100, section="Articles", action="List"):
    return f"{simpsons_base_url}/api/v1/{section}/{action}?limit={limit}&{params if params else ''}"


class Episode(object):
    semaphore = None
    loop = None

    def __init__(self, page_id, name, url):
        self.loop = asyncio.get_event_loop()
        if any(map(lambda el: el is None, [self.semaphore])):
            raise AttributeError("Initialize Class-wide variables!")
        self.name = name
        self.page_id = page_id
        self.url = url

    async def start(self):
        return await self.parse()

    async def parse(self):
        async with self.semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{simpsons_base_url}{self.url}/Quotes") as resp:
                    if resp.status != 200:
                        print("No Quotes for url", self.name, self.url)
                        return None
                    try:
                        data_quotes = await resp.text()
                    except aiohttp.ClientConnectionError as err:
                        print(f"Failed to get {self.name} {self.url} \n", err)
                async with session.get(
                    f"{simpsons_base_url}{self.url}/Appearances"
                ) as resp:
                    if resp.status != 200:
                        print("No Appearances for url", self.name, self.url)
                        return None
                    try:
                        data_appr = await resp.text()
                    except aiohttp.ClientConnectionError as err:
                        print(f"Failed to get {self.name} {self.url} \n", err)

        return (
            None
            if self.url.startswith("/wiki/File:")
            or self.url.startswith("/wiki/Category:")
            else EpisodeModel(
                name=self.name,
                page_id=self.page_id,
                response_quotes=data_quotes,
                response_appearances=data_appr,
                url=self.url,
            )
        )


class EpisodeListing(object):
    semaphore = None
    loop = None

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        if any(map(lambda el: el is None, [self.semaphore])):
            raise AttributeError("Initialize Class-wide variables!")
        self.session = Session()

    async def start(self):
        await self.get_listing()

    async def get_listing(self):
        async with self.semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    get_url("category=Episodes", limit=1500)
                ) as resp:
                    data = await resp.json()

        self.targets = [
            Episode(entry["id"], entry["title"], entry["url"])
            for entry in data["items"]
            if "Season_" not in entry["title"]
            and "Unproduced_episodes" not in entry["title"]
        ]
        tasks = [target.start() for target in self.targets]
        episodes = await asyncio.gather(*tasks)
        self.session.add_all([episode for episode in episodes if episode])
        self.session.commit()
        return


class Character(object):
    semaphore = None
    loop = None

    def __init__(self, page_id, name, url):
        self.loop = asyncio.get_event_loop()
        if any(map(lambda el: el is None, [self.semaphore])):
            raise AttributeError("Initialize Class-wide variables!")
        self.name = name
        self.page_id = page_id
        self.url = url

    async def start(self):
        return await self.parse()

    async def parse(self):
        async with self.semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    get_url(f"id={self.page_id}", action="AsSimpleJson")
                ) as resp:
                    try:
                        data = json.dumps(await resp.json())
                    except aiohttp.ClientConnectionError as err:
                        print(f"Failed to get {self.name} \n", err)
                async with session.get(f"{simpsons_base_url}{self.url}") as resp:
                    try:
                        html_data = await resp.text()
                    except aiohttp.ClientConnectionError as err:
                        print(f"Failed to get {self.name} \n", err)

        return (
            None
            if self.url.startswith("/wiki/File:")
            or self.url.startswith("/wiki/Category:")
            or self.url.startswith("/wiki/Season")
            else CharacterModel(
                name=self.name,
                page_id=self.page_id,
                response=data,
                url=self.url,
                response_html=html_data,
            )
        )


class CharacterListing(object):
    semaphore = None
    loop = None

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        if any(map(lambda el: el is None, [self.semaphore])):
            raise AttributeError("Initialize Class-wide variables!")
        self.session = Session()

    async def start(self):
        await self.get_listing()

    async def get_listing(self):
        async with self.semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    get_url("category=Recurring_characters", limit=1500)
                ) as resp:
                    data = await resp.json()

        self.targets = [
            Character(entry["id"], entry["title"], entry["url"])
            for entry in data["items"]
        ]
        tasks = [target.start() for target in self.targets]
        chars = await asyncio.gather(*tasks)
        self.session.add_all([char for char in chars if char])
        self.session.commit()
        return


class Worker(object):
    def __init__(self, concurrency=None):
        CharacterListing.semaphore = asyncio.Semaphore(concurrency)
        Character.semaphore = asyncio.Semaphore(concurrency)
        EpisodeListing.semaphore = asyncio.Semaphore(concurrency)
        Episode.semaphore = asyncio.Semaphore(concurrency)
        self.loop = asyncio.get_event_loop()

    async def start(self):
        await EpisodeListing().start()
        # await CharacterListing().start()


@click.command()
@click.option(
    "-c",
    "--concurrency",
    type=click.INT,
    default=20,
    help="Number of concurrent connections.",
)
def main(concurrency):
    w = Worker(concurrency)
    asyncio.get_event_loop().run_until_complete(w.start())


if __name__ == "__main__":

    main()
