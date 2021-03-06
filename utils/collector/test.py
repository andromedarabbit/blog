SOURCE_FILE = "D:\\temp\\twitter\\tweet.js"
OUTPUT_DIR = "D:\\repos\\blog\\content\\aside\\"
TWITTER_USERNAME = 'roytang'

import frontmatter
import json

import requests
import urllib.request
import sys

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_final_url(url):
    try:
        response = urllib.request.urlopen(url)
        return response.geturl(), True
    except:
        e = sys.exc_info()[0]
        print("Error: " + url)
        print(e)
        return url, False

with open(SOURCE_FILE, encoding='utf-8') as f:
    d = json.load(f)
    idx = 0
    for d1 in d:
        content = d1["full_text"]

        post = frontmatter.Post(d1["full_text"])
        post['date'] = d1["created_at"]
        post['source'] = 'twitter'
        post['id'] = d1["id_str"]

        post['source_url'] = "https://twitter.com/%s/statuses/%s/" % (TWITTER_USERNAME, post['id'])

        tags = []
        for ht in d1["entities"]["hashtags"]:
            tags.append(ht["text"])
        if len(tags) > 0:
            post['tags'] = tags

        media = []
        if "extended_entities" in d1:
            for m in d1["extended_entities"]["media"]:
                media.append(m["media_url_https"])
        post['media'] = media

        # replies
        post["reply"] = False
        for prop in ["in_reply_to_status_id_str", "in_reply_to_screen_name"]:
            if prop in d1:
                post[prop] = d1[prop]
                post["reply"] = True

        # handle retweet
        post["retweet"] = False
        if content.startswith("RT @"):
            post["retweet"] = True
            colon_idx = content.find(":")
            retweeted_screen_name = content[4:colon_idx]
            mdlink = "[@%s](https://twitter.com/%s/)" % (retweeted_screen_name, retweeted_screen_name)
            # blockquote the content
            rt_content = content[colon_idx+1:]
            content = "RT @%s" % (retweeted_screen_name) # the 'entities' code below should turn this into a link
            content = content + '\n\n> ' + rt_content

        if "entities" in d1:
            # replace mentions with link
            for m in d1["entities"]["user_mentions"]:
                screen_name = m["screen_name"]
                # replace with markdown link
                mdlink = "[@%s](https://twitter.com/%s/)" % (screen_name, screen_name)
                content = content.replace("@"+screen_name, mdlink)
            # clean urls
            for u in d1["entities"]["urls"]:
                url = u["url"]
                expanded_url = u["expanded_url"]
                expanded_url, no_errors = get_final_url(expanded_url)

                if expanded_url.startswith("https://twitter.com/") and expanded_url.find("/status/") > 0 and no_errors:
                    # handle QTs by creating a markdown embed
                    qtid = expanded_url[expanded_url.find("/status/")+8:]
                    # remove ? query params if it exists
                    if qtid.find("?") > 0:
                        qtid = qtid.split("?")[0]
                    if qtid.endswith("/"):
                        qtid = qtid[:-1]
                    # finally, make sure the qtid is a numeric string
                    if not is_number(qtid):
                        content = content.replace(url, expanded_url)
                    else:
                        mdembed = "{{< tweet %s >}}" % qtid
                        content = content.replace(url, mdembed)
                else:
                    content = content.replace(url, expanded_url)

        post.content = content
        newfile = frontmatter.dumps(post)
        with open(OUTPUT_DIR + d1["id_str"] + ".md", "w", encoding='utf-8') as w:
            w.write(newfile)

        idx = idx + 1
        if idx > 100:
            break
