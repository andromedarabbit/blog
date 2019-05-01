# Reference: https://elbauldelprogramador.com/en/how-to-parse-frontmatter-with-python/
from pathlib import Path
import frontmatter
import io

default_category='Just Another Day'

cats_map = {
    "Books" : "Pop Culture",
    "Comics": "Pop Culture",
    "Hardware": "Tech Life",
    "Job Hunting": "", # empty means throw it to default cat if no other cats
    "Learning Things": "Self-Improvement",
    "Legacy Blog Posts": "",
    "Movies": "Pop Culture",
    "Music": "Pop Culture",
    "Nostalgia": "",
    "Politics": "Opinions",
    "Puzzles": "Tech Life", # das weird
    "Review" : "",
    "TV Series": "Pop Culture",
    "Current Events": "",
    "Myself": ""
}

def clean_categories():
    cwd = Path.cwd() 
    # navigate to ./content/posts
    p = cwd / "content" / "post"
    for mdfile in p.glob("**/*.md"):
        print(str(mdfile))
        with mdfile.open() as f:
            try:
                post = frontmatter.load(f)
            except:
                print("Error parsing file")
                continue

            has_changes = False

            tags = []
            if post.get("tags") != None:
                tags = post.get("tags")
                if type(tags) == str:
                    tags = [tags] # standardize to a list

            newcats = []
            if post.get('categories') == None:
                # post['categories'] = [default_category]
                # has_changes = True
                pass
            else: # Categories exists
                cats = post['categories']
                if type(cats) == str:
                    cats = [cats] # standardize to a list

                for cat in cats:
                    has_changes = True
                    if cat == default_category:
                        continue
                    if cat not in tags:
                        tags.append(cat)
                    # if cats_map.get(cat) == None: # no changes, copy over as-is
                    #     if cat not in newcats:
                    #         newcats.append(cat)
                    # else:
                    #     newcat = cats_map[cat]
                    #     # old cat is now a tag
                    #     tags.append(cat)
                    #     has_changes = True
                    #     if len(newcat) > 0:
                    #         # move to new cat
                    #         if newcat not in newcats:
                    #             newcats.append(newcat)
                    #     else:
                    #         # move to default cat if no other cats
                    #         if len(cats) == 1:
                    #             newcats.append(default_category)
                newcats = [] # no more cats!

            if len(tags) > 0:
                post['tags'] = tags
            # if len(newcats) > 0:
            #     post['categories'] = newcats
            post['categories'] = [] # no more cats!

            # print(post['categories'])
            print(post.get('tags'))

            # Save the file.
            if has_changes:
                newfile = frontmatter.dumps(post)
                with mdfile.open("w") as w:
                    w.write(newfile)

clean_categories()    