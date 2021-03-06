import frontmatter
import json
import requests
import urllib.request
from urllib.parse import urlparse, parse_qs, urldefrag
from urllib.error import HTTPError
import sys
from pathlib import Path
import os, shutil
import inspect
from datetime import datetime
import re

from utils import loadurlmap, add_syndication, get_content, add_to_listmap, contentdir
from utils import MDSearcher, URLResolver, PostBuilder, CommentBuilder
urlmap = loadurlmap(False)

def import_plurks():
    resolver = URLResolver()
    searcher = MDSearcher(resolver=resolver)
    importdir = Path("D:\\temp\\plurk-roytang-backup\\data\\plurks")
    matched = []
    unmatched = []
    for jsfile in importdir.glob("**/*.js"):
        with jsfile.open() as f:
            rawjs = f.read()
            splitidx = rawjs.find("=")
            rawjs = rawjs[splitidx+1:-1]
            plurks = json.loads(rawjs)
            for plurk in plurks:
                # if plurk["base_id"] != "9ah6mc":
                #     continue
                plurk_url = "https://plurk.com/p/%s" % plurk["base_id"]
                if plurk_url in urlmap:
                    # no need to do anything, already syndicated
                    continue
                plurk["plurk_url"] = plurk_url
                d = datetime.strptime(plurk['posted'], "%a, %d %b %Y %H:%M:%S %Z")
                datestr = d.strftime("%Y-%m-%d")
                info = searcher.find_by_day_and_text(datestr, plurk['content_raw'])
                if info is None:
                    datestr = d.strftime("%Y-%m")
                    info = searcher.find_by_month_and_text(datestr, plurk['content_raw'])
                if info is not None:
                    matched.append((plurk, info))
                else:
                    post = PostBuilder(plurk["base_id"], source="plurk", content=plurk["content_raw"])
                    post.date = d
                    post.add_syndication("plurk", plurk_url)
                    post.resolve_links(resolver)
                    post.save()
    # print(json.dumps(matched, indent=2))
    for match in matched:
        plurk = match[0]
        info = match[1]
        add_syndication(Path(info["file"]), plurk["plurk_url"], "plurk")
    # print(json.dumps(unmatched, indent=2))
    print(len(matched))
    print(len(unmatched))
    resolver.save_cache()

    # with Path("D:\\temp\\plurk-unmatched.json").open("w", encoding="UTF-8") as f:
    #     f.write(json.dumps(unmatched, indent=2))

def import_plurk_comments():
    importdir = Path("D:\\temp\\plurk-roytang-backup\\data\\responses")
    for jsfile in importdir.glob("**/*.js"):
        parent_id = jsfile.stem
        # if parent_id != "9wk9ys":
        #     continue
        parent_url = "https://plurk.com/p/%s" % (parent_id)
        if parent_url in urlmap:
            parent_info = urlmap[parent_url]
            with jsfile.open() as f:
                rawjs = f.read()
                splitidx = rawjs.find("=")
                rawjs = rawjs[splitidx+1:-1]
                reacts = json.loads(rawjs)
                for react in reacts:
                    cb = CommentBuilder(contentdir / parent_info['source_path'])
                    date = datetime.strptime(react['posted'], "%a, %d %b %Y %H:%M:%S %Z")
                    author_name = react['user'].get('display_name')
                    if author_name is None:
                        author_name = react['user'].get('nick_name')
                    author = {
                        "name": author_name,
                        "url": "https://plurk.com/%s" % (react['user']['nick_name']),
                        "photo": "https://avatars.plurk.com/%s-small%s.gif" % (react['user']['id'], react['user']['avatar']),
                    }
                    cb.add_comment(react['id'], date, author, "plurk", react['content_raw'], url=parent_url , overwrite=True)


        else:
            print("### ERROR: Missing parent file for %s" % str(jsfile))

#import_plurks()

import_plurk_comments()
