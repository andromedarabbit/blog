sourcefolder = "D:\\temp\\tumblr"
base_url = "http://roytang.net"

import xmltodict
import frontmatter
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
import urllib
import shutil
import os
import json

from html.parser import HTMLParser

class MyParser(HTMLParser):
    def __init__(self, output_list=None):
        HTMLParser.__init__(self)
        if output_list is None:
            self.output_list = []
        else:
            self.output_list = output_list
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.output_list.append(dict(attrs).get('href'))

blogdir = Path(os.environ['HUGO_BLOG_OUTDIR'])
urlmapfile = blogdir / "urlmap.json"

sourcedir = Path(sourcefolder)
postsfile = sourcedir / "posts.xml"
mediadir = sourcedir / "media"

cwd = Path.cwd()
contentdir = cwd / "content"

def get_final_url(url):
    try:
        response = urllib.request.urlopen(url)
        return response.geturl()
    except:
        print("Error: " + url)
        return url

def create_photo_post(p):
    kind = "photos"
    content = p.get('photo-caption', '')
    post = frontmatter.Post(content)
    d = datetime.strptime(p["@date-gmt"], "%Y-%m-%d %H:%M:%S %Z")
    post['date'] = d
    post['syndicated'] = [
        {
            "type": "tumblr",
            "url": p["@url-with-slug"]
        }
    ]

    tags = p.get("tag", [])
    if not isinstance(tags, list):
        tags = [tags]
    if len(tags) > 0:
        post["tags"] = tags

    post["source"] = "tumblr"
    if "photo-link-url" in p:
        post["photo_link_url"] = p["photo-link-url"]
    id = p["@id"]

    outdir = contentdir / kind / d.strftime("%Y") / d.strftime("%m") / id
    if not outdir.exists():
        outdir.mkdir(parents=True)
    outfile = outdir / "index.md"

    newfile = frontmatter.dumps(post)
    with outfile.open("w", encoding="UTF-8") as w:
        w.write(newfile)

    # find photos
    for imgfile in mediadir.glob(id + "*.*"):
        to_file = outdir / imgfile.name
        shutil.copy(str(imgfile), str(to_file))    


def create_post(p, kind, content, params):
    post = frontmatter.Post(content)
    d = datetime.strptime(p["@date-gmt"], "%Y-%m-%d %H:%M:%S %Z")
    post['date'] = d
    post['syndicated'] = [
        {
            "type": "tumblr",
            "url": p["@url-with-slug"]
        }
    ]

    tags = p.get("tag", [])
    if not isinstance(tags, list):
        tags = [tags]
    if len(tags) > 0:
        post["tags"] = tags

    post["source"] = "tumblr"
    id = p["@id"]
    for param in params:
        post[param] = params[param]
    outdir = contentdir / kind / d.strftime("%Y") / d.strftime("%M")
    if not outdir.exists():
        outdir.mkdir(parents=True)
    outfile = outdir / ( id + ".md" )
    newfile = frontmatter.dumps(post)
    with outfile.open("w", encoding="UTF-8") as w:
        w.write(newfile)

def add_syndication(mdfile, url, stype):
    #print(str(mdfile))
    with mdfile.open(encoding="UTF-8") as f:
        try:
            post = frontmatter.load(f)
        except:
            print("Error parsing file")
            return

        if post.get('syndicated') == None:
            post['syndicated'] = []
        else:
            for s in post['syndicated']:
                if s["type"] == stype and s["url"] == url:
                    # dont add a duplicate!
                    return

        post['syndicated'].append({
            'type': stype,
            'url': url
        })
        newfile = frontmatter.dumps(post)
        with mdfile.open("w", encoding="UTF-8") as w:
            w.write(newfile)

urlmap = {}
with urlmapfile.open(encoding="UTF-8") as f:
    tempurlmap = json.loads(f.read())
    for u in tempurlmap:
        u1 = tempurlmap[u]
        if "syndicated" in u1:
            for s in u1['syndicated']:
                if 'url' in s:
                    su = s['url']
                    urlmap[su] = u1
        urlmap[u] = u1

countbytype = {}
reblogscount = 0
instagramcount = 0
roytangcount = 0
unprocessed = 0

def import_post(post):

    global countbytype
    global reblogscount
    global instagramcount
    global roytangcount
    global unprocessed
    global urlmap

    ptype = post['@type']
    tags = post.get("tag", [])
    if len(tags) == 0:
        return
    for tag in tags:
        if tag not in ["IFTTT", "Instagram"]:
            return

    unprocessed = unprocessed + 1

    if ptype == 'photo':
        if 'photo-link-url' in post:
            url = post['photo-link-url']
            print(url)
            if url.startswith("https://www.instagram.com/"):
                url = urlparse(url)
                url = "https://instagram.com" + url.path
                u = urlmap[url]

                source_path = Path(u['source_path'])
                full_path = contentdir / source_path
                add_syndication(full_path, post['@url-with-slug'], "tumblr")
                instagramcount = instagramcount + 1
                return

        if 'photo-caption' in post:
            text = post['photo-caption']
            p = MyParser()
            p.feed(text)
            for u in p.output_list:
                url = get_final_url(u)
                if url.startswith("https://www.instagram.com/"):
                    # remove my username as needed
                    url = url.replace("/roytang0400", "")
                    url = urlparse(url)
                    url = "https://instagram.com" + url.path
                    u = urlmap[url]

                    source_path = Path(u['source_path'])
                    full_path = contentdir / source_path
                    add_syndication(full_path, post['@url-with-slug'], "tumblr")
                    instagramcount = instagramcount + 1
                    return


    return

    if ptype == 'link':
        if 'link-url' in post and post['link-url'].find("://roytang.net") >= 0:
            link_url = urlparse(post['link-url'])
            u = urlmap[link_url.path]
            source_path = Path(u['source_path'])
            full_path = contentdir / source_path
            add_syndication(full_path, post['@url-with-slug'], "tumblr")
            roytangcount = roytangcount+1
            return
        else:
            if 'link-url' in post:
                # print('link: %s :: %s' % (post['link-url'], post['@url-with-slug']) )
                # create_post(
                #     post,
                #     "links",
                #     post.get('link-description', ''),
                #     {
                #         "link-url": post.get('link-url', ''),
                #         "link-text": post.get('link-text', '')
                #     }
                # )
                return

    if post['@is_reblog'] == 'true':
        reblogscount = reblogscount + 1
        return

    if ptype == 'photo':
        #create_photo_post(post)
        return

    if ptype == 'regular':
        if 'regular-title' in post:
            #print(post['regular-title'])
            create_post(post, "post", post.get('regular-body', ''), { 'title': post.get('regular-title', '') })
            return
        else:
            create_post(post, "notes", post.get('regular-body', ''), {})

    if ptype == 'quote':
        #print(post['quote-text'])
        pass

    if ptype == 'answer':
        # print(post)
        pass

    unprocessed = unprocessed + 1
    if ptype not in countbytype:
        countbytype[ptype] = 1
    else:
        countbytype[ptype] = countbytype[ptype] + 1


with postsfile.open(encoding="UTF-8") as fd:
    doc = xmltodict.parse(fd.read())
    posts = doc['tumblr']['posts']['post']
    for post in posts:
        import_post(post)


print("total posts: " + str(len(posts)))
print("total reblogs: " + str(reblogscount))
print("total instagram: " + str(instagramcount))
print("total roytang.net: " + str(roytangcount))
print("total unprocessed: " + str(unprocessed))
print(countbytype)
