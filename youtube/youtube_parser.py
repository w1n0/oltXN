from youtube_search import YoutubeSearch
import hashlib


def searcher(text):
    res = YoutubeSearch(text, max_results=10).to_dict()
    return res
