import json
import sys
from string import Template
from CreatorPipeline import _openai

# prompt:
intents = [
    [
        "Backing up data",
        "Fear of Losing work or progress due to technical issues or software crashes.",
    ],
    [
        "Handling Negative Criticism",
        "Fear of Receiving negative feedback or criticism of their work.",
    ],
    [
        "Falling Behind Peers",
        "Fear of Not being able to keep up with the fast-paced nature of the industry and changes in technology.",
    ],
    [
        "Failing At Freelance",
        "Fear of Failing to meet client expectations or requirements.",
    ],
    [
        "Finding Clients",
        "Fear of Difficulty in finding a steady stream of work or clients.",
    ],
    [
        "Finding CG Work",
        "Fear of Struggling to make a living as a freelance 3D artist.",
    ],
    [
        "Standing Out as an Artist",
        "Fear of Difficulty in coming up with new and innovative ideas for their work.",
    ],
    [
        "Work Productivity tips",
        "Fear of Being unable to produce high-quality work within tight deadlines.",
    ],
    [
        "Technical Skill Growth",
        "Fear of Not having the necessary skills or experience to take on certain projects.",
    ],
    [
        "avoid Work Burnout",
        "Fear of Losing motivation or passion for 3D art due to burnout or creative fatigue.",
    ],
    [
        "Become More Hireable",
        "Fear of being unable to differentiate themselves from competitors in the industry.",
    ],
    [
        "improve Job Security",
        "Fear of being replaced by advances in artificial intelligence and automation.",
    ],
    ["Work-Life Balance", "Fear of Difficulty in maintaining a work-life balance."],
    [
        "stop Impostor Syndrome",
        "Feeling overwhelmed by the amount of competition in the industry.",
    ],
    [
        "Learning new Software",
        "Fear of not being able to keep up with the constant changes and updates to industry software and tools.",
    ],
    [
        "Improve 3D Skills",
        "Fear of not being talented or creative enough to succeed in the field.",
    ],
    [
        "Improve Skills Quickly",
        "Anxiety about the amount of work required to master 3D art and software.",
    ],
    [
        "Study Hacks",
        "Fear of falling behind in class or not being able to keep up with the curriculum.",
    ],
    [
        "Better Art Fast",
        "Fear of Difficulty in finding a job after graduation or securing a successful career in the industry.",
    ],
    [
        "Money Saving Tips",
        "Fear of not being able to afford the necessary equipment and software for the field.",
    ],
    [
        "Dont Compare Yourself",
        "Feeling overwhelmed by the amount of competition in the industry.",
    ],
    [
        "Career Growth",
        "Fear of not being able to differentiate themselves from other graduates in the field.",
    ],
    [
        "Skill Growth",
        "Fear of not having the necessary skills or experience to succeed in the industry.",
    ],
    [
        "Taking Feedback",
        "Anxiety about being able to handle criticism and feedback on their work.",
    ],
    [
        "Networking",
        "Fear of Difficulty in finding a mentor or support system in the field.",
    ],
    [
        "Artist Financial Freedom",
        "Anxiety about being able to afford or manage student debt.",
    ],
    [
        "School-Life Balance",
        "Fear of not being able to balance their studies with other aspects of their life.",
    ],
    ["3D Art Skills", "Desire for Developing technical skills"],
    ["Best Practices Portfolio", "Desire for Building a strong portfolio"],
    [
        "Networking tips",
        "Desire for Networking with professionals and peers in the industry",
    ],
    [
        "Skill Mastery",
        "Desire for Specializing in a specific area, such as character modeling or environment design",
    ],
    [
        "Artist Business Skills",
        "Desire for Learning the business side of the industry, such as contracts and project management",
    ],
    [
        "Finding Relevant work",
        "Desire for Working on real-world projects to gain experience",
    ],
    [
        "Invent New Tech",
        "Desire for Experimenting and pushing boundaries with new techniques and styles",
    ],
    [
        "Find 3D Events",
        "Desire for Attending workshops and conferences to learn from industry experts",
    ],
    [
        "Artist Collab",
        "Desire for Collaborating with other artists and designers on projects",
    ],
    [
        "Learn 3D Printing",
        "Desire for Using 3D printing technology to bring designs to life",
    ],
    [
        "Learn Virtual Production",
        "Desire for Learning to work with virtual reality and augmented reality technology",
    ],
    ["Find art style", "Desire for Developing a unique artistic voice and style"],
    [
        "Publish Experience Book",
        "Desire for Getting published in industry publications or online galleries",
    ],
    [
        "Best 3D Competitions",
        "Desire for Participating in contests and challenges to showcase skills",
    ],
    ["Land Dream Job", "Desire for Working for a top animation or game studio"],
    ["Freelancing Startup Tips", "Desire for Becoming a freelance 3D artist"],
    ["Become 3D Teacher", "Desire for Teaching 3D art to others as a career path"],
    [
        "Organize Shortfilm Team",
        "Desire for Using 3D software to create 3D animations or short films",
    ],
    [
        "Becoming VFX Influencer",
        "Desire for Building a strong online presence through social media and a personal website",
    ],
    [
        "Learn new Technology",
        "Desire for Continuing education and staying up-to-date with industry trends and advancements.",
    ],
]
# https://colab.research.google.com/drive/1vQwddMAPSN-Z4LcSXg80Zj1hTfuUmx3s?usp=sharing#scrollTo=NNsuuLPc5pvv

# Steps for Script
# Take database info and prior prompts store wherever,
# generate chapters -> markers
# expand chapters into a script

# Research
# GAIN
# GOAL1
# GOAL2
# TITLE

# Prompts:

# Reccomended_Titles = "With the end goal of {GAIN} in mind, Write 10 Youtube Video Title Ideas that are similar to the following: "
# Intent_SERP = "using careful consideration, summarize these search results and summarize the statistically most likely goal of the person who made the search: "
# Intent_Title = "How similar are these two goals:\n1) {GOAL1},\n2) {GOAL2}"
# Brand_Check = "Out of the following websites, does a large brand have the majority of results?"
# Talking_Points = "From the following topic, please give me a 3 chapter outline of talking points with the intent of {GOAL2}: "
# Script_Draft = "With the call to action of {GAIN} in mind, write an rough draft for a youtube script whose video title is {TITLE}. Take the following Chapters and expand upon them in the script."
# Thumbnail_Desc = "Come up with three descriptions for a thumbnail image for a youtube video whose title is: "
# sub description using keywords and chapter summary
# "Can you summarize the intent of the following. Provide only a singular result"
# "Does that match this: {}"
# "Is your summary related to {}"
# "Can you suggest ten Youtueb Video Titles based on your summarized intent? Keep all results within 60 Characters. For each title, provide a short 100 character description."
# "Based on your first result, can you draft 3 key talking points chapter titles with supporting content?"
# "can you provide this same answer in a code block using markdown"
# #save file
# "What keywords and hashtags should i use for marketing this video?"
# "can you rewrite this episode as a blog post?"
# "What are the biggest solo youtube channels for this topic? exclude any large companies"
# "can you do a Youtube Video SERP analysis for the topic 'learn computer animation' and suggest ten Youtube Video Titles from those results?"

# "With the end goal of '{GOAL}' in mind, Write 5 youtube video titles (under 80 characters) with a description (under 100 characters), include 3 bulleted chapters (under 50 characters). Use SERP analysis from google, youtube videos, and top youtube channels to derive your results. The keyword phrase is: '{KEYWORD_PHRASE}'. Make sure you satisfy the viewers {FEEL}: {INTENT}. Format the results using json in a code block. use only keys like videos, title, description, chapters in the json"
# "What are the top 30 struggles that graphic designers face?"


# Define is going to be fairly manual, use vidiq or something to reccomend.
# eventually have a suggestion based on top competitor videos, but that will be discovered in research.


# Steps for research

# Query Youtube Video about keyword
# Query Youtube Channels about Keyword
# Query Google SERP about keyword
# Query Channel Top Viewed Videos( if keyword?? )
# derive Title & Descriptions (& Script?)
# is it possible to derive CC? ((download video and transcribe it?))

# Sentencize
# Tokenize
# Cluster by 1, 2 and 3 word phrases
#   these solve for intent and similar keywords
# prompt check from titles
# generate prompts in succession
# aim to only make thumbnail and titles for this step.
# extract whatever data to database

GOAL = "gaining subscribers"
_prompt = Template(
    """
With the end goal of '$GOAL' in mind, Write 5 youtube video titles (under 80 characters) \
with a description (under 100 characters), include 3 bulleted chapters (under 50 characters). \
Use SERP analysis from google, youtube videos, and top youtube channels to derive your results. \
The keyword phrase is: '$KEYWORD_PHRASE'. Make sure you satisfy the viewers $INTENT. \
Format the results using json in a code block. use only keys like videos, title, description,\
chapters in the json."
"""
)


def recursive_keywords():
    """Generates the initial text ideas for an episode using OpenAI."""
    failed = False
    for i, concept in enumerate(intents):
        print(f"trying {i}", file=sys.stderr)
        try:
            with open(f"../_local/results/ideas_{i:04}.json", "r") as f:
                data = json.load(f)
            if data:
                continue
        except json.decoder.JSONDecodeError:
            pass

        KEYWORD_PHRASE, INTENT = concept
        prompt = _prompt.substitute(
            GOAL=GOAL, KEYWORD_PHRASE=KEYWORD_PHRASE, INTENT=INTENT
        )
        # save json
        try:
            data = _openai.generate_text(prompt)
            with open(f"../_local/results/ideas_{i:04}.json", "w") as f:
                json.dump(json.loads(data), f, indent=4)
        except Exception as err:
            failed = True
            print(err)
    if failed:
        print("do it again", file=sys.stderr)
        recursive_keywords()
