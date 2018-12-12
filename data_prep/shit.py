import io
import json
import re
import sqlite3
from urllib import error, request

import networkx as nx
import requests
from bs4 import BeautifulSoup
from networkx.algorithms import bipartite
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.sql import exists

conn = sqlite3.connect("simpsons.sqlite3")
simsons_api_base_url = "https://simpsons.wikia.com/api/v1"


def api_call(params, limit=100, section="Articles", action="List", clean=False):
    url = (
        f"{simsons_api_base_url}/{section}/{action}?{limit}&{params if params else ''}"
        if not clean
        else f"{simsons_api_base_url}/{section}/{params}"
    )
    req = request.Request(url)
    try:
        res = request.urlopen(req).read()
        return json.loads(res.decode("utf-8"))
    except error.HTTPError as err:
        print(err)


def get_character_list():
    characters = []
    json_response = api_call("category=Recurring_characters", limit=1500)
    for character in json_response["items"]:
        characters.append([character["title"], character["id"], character["url"]])

    return characters


def get_episode_list():
    episodes = []
    json_response = api_call("category=Episodes", limit=1000)
    for episode in json_response["items"]:
        episodes.append([episode["title"], episode["id"], episode["url"]])

    return episodes


def get_season_dictionary():
    seasons = {}
    for i in range(1, 31):
        episodes = []
        json_response = api_call(f"category=Season_{i}_episodes")
        for episode in json_response["items"]:
            episodes.append(episode["title"])
        seasons[i] = episodes
    return seasons


# Filling up the lists
seasons = get_season_dictionary()
# Really strange select page_id returns something totally different
characterIds = [
    c[3] for c in conn.cursor().execute("Select * from characters").fetchall()
]
characterNames = [
    c[1] for c in conn.cursor().execute("Select * from characters").fetchall()
]
episodes = get_episode_list()

AppearanceNetwork = nx.Graph()

nameDict = {
    "Simpson Christmas Stories": "Simpsons Christmas Stories",
    "Love is a Many Splintered Thing": "Love is a Many-Splintered Thing",
    "E Pluribus Wiggum": "E. Pluribus Wiggum",
}

nonepisodeDict = {
    "The\xa0Simpsons\xa0Guy": True,
    "The Simpsons Guy": True,
     "The Simpsons Guy\"": True,
    "The Longest Daycare": True,
}

queries = [
    ["SELECT name FROM episodes WHERE name = ?", "name"],
    ["SELECT name FROM episodes WHERE name LIKE ?", "name%"],
    ["SELECT name FROM episodes WHERE name LIKE ?", "%name%"],
]


def sqlquery_for_episode_name(episode_name):
    word_list = [episode_name.strip(), episode_name.replace('"', "")]
    tmp = []
    for query in queries:
        for word in word_list:
            tmp = (
                conn.cursor()
                .execute(query[0], (query[1].replace("name", word),))
                .fetchall()
            )
            if len(tmp) > 0:
                break
        if len(tmp) > 0:
            return tmp

    return tmp


morethanone = {}


def cleanup_episode_name(episode_name):
    if nonepisodeDict.get(episode_name, False):
        return None
    tmp = sqlquery_for_episode_name(episode_name)
    if len(tmp) == 0:
        episode_name = episode_name.replace("D'oh", "(Annoyed Grunt)")
        tmp = sqlquery_for_episode_name(episode_name)
        if (len(tmp)) == 0:
            episode_name = nameDict.get(episode_name, episode_name)
            tmp = sqlquery_for_episode_name(episode_name)
        if len(tmp) == 0:
            episode_name = episode_name.split()
            for i in range(len(episode_name) - 1):
                tmp = sqlquery_for_episode_name(
                    " ".join(episode_name[: len(episode_name) - i])
                )
                if len(tmp) > 0:
                    break

    if len(tmp) > 1:
        if isinstance(episode_name, list):
            morethanone[" ".join(episode_name)] = tmp
        else:
            morethanone[episode_name] = tmp
        print(episode_name, " More than one results: ", tmp)
    if len(tmp) > 0 and (isinstance(tmp[0], list) or isinstance(tmp[0], tuple)):
        return tmp[0][0]
    return None


episode_no_name = set()

# We should somehow find a way to know which element is the right episode list
def build_appearance_network():
    log_file = open("appearance_network_log.txt", "w+")
    episodes_with_problem = []

    for i in range(0, len(characterIds)):
        AppearanceNetwork.add_node(characterNames[i], bipartite=0)
        # print(characterNames[i], characterIds[i])
        response = api_call(params=f"AsSimpleJson?id={characterIds[i]}", clean=True)

        # try:
        for section in response["sections"]:
            lower_title = section["title"].lower()

            if (
                re.match("episode", lower_title) != None
                or re.match("appearance", lower_title) != None
            ):
                if (
                    re.match("non", lower_title) == None
                    and re.match("other", lower_title) == None
                ):
                    # We should somehow find a way to know which element is the right episode list

                    if len(section["content"]) > 1:
                        # print('More section found for this character: ',characterNames[i])
                        log_file.write(
                            f"More section found for this character: {characterNames[i]}\n"
                        )

                    for sublist in section["content"]:  # [-1]['elements']:
                        if sublist["type"] == "list":
                            for episode in sublist["elements"]:
                                episode_name = episode["text"]
                                if re.match("^Episode|^THOH", episode_name) != None:
                                    index = re.search('– "', episode_name)
                                    if index:
                                        if nonepisodeDict.get(episode_name[index.end():], False):
                                            continue
                                        ep_name = cleanup_episode_name(
                                            episode_name[index.end() :]
                                        )
                                        if ep_name:
                                            AppearanceNetwork.add_node(
                                                ep_name, bipartite=1
                                            )
                                            AppearanceNetwork.add_edge(
                                                characterNames[i], ep_name
                                            )
                                            continue
                                    tmp = re.findall('\\".*?\\"', episode_name)
                                    if len(tmp) == 0:
                                        episode_no_name.add(episode_name)
                                        continue

                                    episode_name = tmp[0]
                                    # try:
                                    if nonepisodeDict.get(episode_name, False):
                                        continue
                                    episode_name = cleanup_episode_name(episode_name)
                                    # except:
                                    # if episode_name not in episodes_with_problem:
                                    #     episodes_with_problem.append(episode_name)
                                    # continue
                                    AppearanceNetwork.add_node(
                                        episode_name, bipartite=1
                                    )
                                    AppearanceNetwork.add_edge(
                                        characterNames[i], episode_name
                                    )

        if AppearanceNetwork.degree(characterNames[i]) == 0:
            # print('No appearance for: ', characterNames[i], characterIds[i])
            log_file.write(
                f"No appearance for: {characterNames[i]}, {characterIds[i]}\n"
            )
            AppearanceNetwork.remove_node(characterNames[i])
        # except Exception as error:
        # print('Problem with character:',characterNames[i],characterIds[i])
        # log_file.write(
        # f"Problem with character: {characterNames[i]},{characterIds[i]}\n"
        # )
        # print(error)
    log_file.write("\n Episodes with problem: \n")
    log_file.write("\n".join(episodes_with_problem) + "\n")
    log_file.write("\n\n\n Episodes with more than one: \n")
    for asd in morethanone.keys():
        log_file.write(f"{asd}, {morethanone[asd]} \n\n")
    log_file.write("\n\n\n\n No Name:")
    log_file.write("\n".join(list(episode_no_name)))
    log_file.close()

    # TODO: Homer Simpson


build_appearance_network()
# Save the network to a pickle file for further usage
nx.write_gpickle(AppearanceNetwork, "appearance network")
print()


characters = get_character_list()
episodes = get_episode_list()


def get_links_from_page(wiki_url):
    url = "http://simpsons.wikia.com" + wiki_url

    try:
        res = request.urlopen(url)
    except:  # For edge-cases like: Fit-Fat Tony, Blue-Haired Lawyer
        url = url.replace("_", "-", 1)
        try:
            res = request.urlopen(url)
        except error.HTTPError as err:
            """
            If it's still not enough. See: /wiki/Baron_Von_Kiss_A_Lot or /wiki/Joey_Jo_Jo_Junior_Shabadoo
            The dashes and underscores are messed up in the provided page list
            """
            print("With the page: ", wiki_url)
            print("Problem: ", err)
            return -1

    response_text = res.read().decode("utf-8")
    links = []
    start = response_text.find("WikiaMainContent")
    end = response_text.find('id="Appearances"')
    if end == -1:
        end = response_text.find('id="Episode_Appearances"')
    if end == -1:
        end = response_text.find('id="Episode_appearances"')
    if end == -1:
        end = response_text.find('id="Appearances:"')
    if end == -1:
        end = response_text.find('id="Appearance"')
    if end == -1:
        end = response_text.find('id="Episodes"')
    if end == -1:
        end = response_text.find('id="Apperances"')
    if end == -1:
        end = response_text.find('id="Appearences"')
    if end == -1:
        end = response_text.find('id="Episode.2FGame_Appearances"')

    if end == -1 or start == -1:
        print("Problem with:", wiki_url)
        return -1
    # end = response_text.find('<!-- WikiaMainContent -->')
    soup = BeautifulSoup(response_text[start:end])
    names = [link.get("href") for link in soup.find_all("a")]
    names = [
        link.split("/wiki/")[1]
        if link and "/wiki/" in link and link.startswith("http")
        else link
        for link in names
    ]
    # names = [ link for link in names if  ]

    names = [
        requests.get("https://simpsons.wikia.com" + name).url.split("/wiki/")[1]
        for name in list(set(names))
        if name
        and name.startswith("/wiki/")
        and "/Special:" not in name
        and "/Category:" not in name
        and "/File:" not in name
        and "List_of_Episodes" not in name
        and "Season" not in name
        and "Simpsons_Wiki" not in name
    ]

    names = [
        name
        for name in list(set(names))
        if name
        and not name.startswith("List_of_Episodes")
        and not name.startswith("Category")
        and not name.startswith("File")
        and not name.startswith("Special")
        and not name.startswith("Season")
        and not name.startswith("Simpsons_Wiki")
    ]
    names = [name.split("?")[0] for name in names if name]
    for name in names:

        c = conn.cursor()
        c.execute(f"select name from 'characters' where url = '/wiki/{name}'")
        tmp = c.fetchall()
        # tmp = (
        #     Session()
        #     .query(CharacterModel.url)
        #     .filter(exists().where(CharacterModel.url == "/wiki/" + name))
        #     .first()
        # )
        if len(tmp) > 0:
            links.append(name.replace("_", " "))
    return list(set(links))


# Requires a title with underscores instead of spaces e.g. 'Homer_Simpsons'
# We don't really need this function since we store the id's in a dictionary with the names as keys.
def get_articleId_from_title(title):
    ids = "1"

    json_response = api_call(f"ids={ids}&titles={title}", action="Details")
    id = list(json_response["items"].keys())[1]
    return id


# Creating the network
G = nx.Graph()
G.add_nodes_from(c[0] for c in characters)
# Create network links
i = 0

for c in characters:
    i += 1
    print("Creating network: ", round(i / len(characters) * 100, 2), "%", end="\r")
    links_to_make = get_links_from_page(c[2])
    if (
        links_to_make != -1
    ):  # url doesn't exist or fuckin episodes/appearances is not in a good form
        for l in links_to_make:
            G.add_edge(c[0], l)

# Save the network to a pickle file for further usage
nx.write_gpickle(G, "linknetwork")
