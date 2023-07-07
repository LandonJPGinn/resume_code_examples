"""
The following are small snippets of private repository code.
While these projects cant paint a full example, I hope it can
demonstrate my prefered approaches to scenarios within python.
"""


# Youtube Production Suite
# constants.py

class DefaultLoader:
    """
    Global Singleton Loader for System to access while Production Suite is Live
    """
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(DefaultLoader, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        """Load Youtube Channel configured paths for the project"""
        local_path = Path(__file__).parent
        database = local_path / os.environ["DATABASE_DEFAULTS"]

        with open(database, "rb") as f:
            self.__dict__.update(**tomllib.load(f))

        self.globals()

    def globals(self):
        """Convert config str values to Path Objects for flexible usage"""
        self.root = Path(self.root)
        self.repo_root = Path(self.repo_root)
        self.show_episode_root = Path(self.root) / self.episode_root
        self.code_root = Path(self.code_root)
        self.docs_root = Path(self.code_root).parent.parent
        self.edit_local_area = Path(self.edit_local_area)
        self.edit_remote_area = Path(self.edit_remote_area)
        self.database_root = self.root / self.database_root
        self.database_sync = self.root / self.database_sync
        self.database_episodes = self.root / self.database_episodes
        self.database_categories = self.root / self.database_categories
        self.database_dashboard = self.root / self.database_dashboard
        self.database_playlists = self.root / self.database_playlists
        self.database_statuses = self.root / self.database_statuses
        self.database_active = self.root / self.database_active
        self.template_deliverables = [getattr(self, d) for d in self.deliverables]

        self.thumbnail_graphics = self.root / self.research_graphics_root
        self.thumbnail_fonts = self.root / self.research_thumb_fonts
        self.thumbnail_backgrounds = self.root / self.research_thumb_backgrounds
        self.thumbnail_subjects = self.root / self.research_thumb_subjects
        self.episode_release_schedule_path = self.repo_root / self.episode_release_schedule_path

    def load_episode_defaults(self, episode=None):
        if episode:
            if episode.abbrv_title == Path(self.episode_root).name:
                self.episode_root = self.episode_root
            else:
                self.episode_root = self.root / self.episode_root / episode.abbrv_title
        else:
            self.episode_root = Path.cwd()

        episodic = self.episode_root / self.episodic_check
        if not episodic.exists():
            self.thumbnail_topics = ""
            self.thumbnail_output = ""
            return

        self.thumbnail_topics = self.episode_root / self.research_thumb_topics
        self.thumbnail_output = self.episode_root / self.research_thumb_output


class Platform:
    """Config Loader for Social Platforms. ie. Youtube, Buzzsprout, Twitter"""
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Platform, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        local_path = Path(__file__).parent.parent / os.environ["PLATFORM_SECRETS"]
        for platform_path in local_path.rglob("*.toml"):
            name = platform_path.stem.split("_")[-1]
            with open(platform_path, "rb") as f:
                self.__dict__.update({name: tomllib.load(f)})

        for client_path in local_path.rglob("*secrets.json"):
            with open(client_path, "rb") as f:
                self.__dict__.update({"client": json.load(f)})

        self.client_secret = Path(self.youtube["client_secret"]).expanduser().resolve()


class Prompts:
    """OpenAI Prompt Template Loader"""
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Prompts, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        prompt_path = Path(__file__).parent.parent / os.environ["PROMPT_TEMPLATES"]
        with open(prompt_path, "rb") as f:
            data = tomllib.load(f)

        for k, v in data.items():
            if isinstance(v, str):
                data[k] = Template(v)

        self.__dict__.update(**data)



# Publisher.py
"""Simplification Layer for PublishFactory."""
import pprint

from platforms.__youtube import YoutubeEpisodePublisher
from platforms.__buzzsprout import BuzzsproutEpisodePublisher

pp = pprint.PrettyPrinter(indent=4)


class PublishError:
    def publish(self):
        print("Error Occured. Check Release Params:")
        pp.pprint(self.params)


class PublishVideoYT:
    def publish(self):
        YEP = YoutubeEpisodePublisher(self.params)
        YEP.publish_video()


class PublishShortYT:
    def publish(self):
        YEP = YoutubeEpisodePublisher(self.params)
        YEP.publish_video()


class PublishMessageYT:
    def publish(self):
        YEP = YoutubeEpisodePublisher(self.params)
        YEP.publish_message()


class PublishPodcastBuzzsprout:
    def publish(self):
        BEP = BuzzsproutEpisodePublisher(self.params)
        BEP.publish()

_publishFactory = {
    "Youtube Video": PublishVideoYT,
    "Youtube Short": PublishShortYT,
    "Youtube Message": PublishMessageYT,
    "Buzzsprout Podcast": PublishPodcastBuzzsprout,
    "Error": PublishError,
}

class PublishFactory:
    def __new__(cls, params):
        obj = _publishFactory.setdefault(params.get("_platform", None), "Error")
        publish_object = super(PublishFactory, cls).__new__(obj)
        publish_object.params = params
        return publish_object

    def publish(self):
        ...


# database.py

class DatabaseSynchronizer:
    """Synchronizes local database with online database"""

    def __init__(self):
        """Initializes the database synchronizer
        """
        _handler = DatabaseHandler()
        self.online = _handler.online
        self.local = _handler.local

    def is_local_current(self):
        return self.online.latest == self.local.latest

    def sync_local(self):
        print(f"Store to local {DEFAULTS.database_episodes}")

        """stores information from online into local db. set Sync Timestamp in state worksheet"""
        DEFAULTS.database_categories.write_text("\n".join(self.online.categories))
        DEFAULTS.database_playlists.write_text("\n".join(self.online.playlists))
        DEFAULTS.database_statuses.write_text("\n".join(self.online.statuses))
        json.dump(
            self.online.dashboard,
            DEFAULTS.database_dashboard.open(mode="w"),
            indent=4,
        )
        json.dump(
            self.online.episodes,
            DEFAULTS.database_episodes.open(mode="w"),
            indent=4,
        )

        self.online.timestamp()

        json.dump(
            self.online.state_timestamp,
            DEFAULTS.database_sync.open(mode="w"),
            indent=4,
        )


#_openai.py

openai.api_key = PLATFORMS.openai.get("OPENAI_KEY")


def generate_text(prompt, output=None):
    response = openai.Completion.create(
        model="text-davinci-003", prompt=prompt, max_tokens=1000
    )
    if not output:
        return response.choices[0].text
    with open(output, "w") as f:
        f.write(response.choices[0].text)


def generate_image(prompt, n, prefix="default", output=None):
    response = openai.Image.create(prompt=prompt, n=n, size="1024x1024")
    image_urls = response["data"][0]["url"]

    if not output:
        return image_urls

    for i, pic in enumerate(image_urls):
        pic_path = Path(f"{output}") / f"{prefix}_{i:04d}.png"
        save_image(pic_url=pic, output=pic_path)


def transcribe_audio(fp, output=None):
    with open(fp, "rb") as f:
        response = openai.Audio.transcribe(model="whisper-1", file=f)
        if response:
            print(response)
            return response


def translate_audio(file, lang="English", output=None):
    openai.Audio.translate(model="whisper-1", file=file, language=lang)


def save_image(pic_url, output):
    with open(output, "wb") as handle:
        response = requests.get(pic_url, stream=True)

        if not response.ok:
            print(response)
            return -1

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)

    return 0


# Personal OpenAI Cellphone Number Personality
# app.py
import os
from datetime import datetime
from string import Template

import openai
from dotenv import load_dotenv
from flask import Flask, Response, request
from twilio.twiml.messaging_response import MessagingResponse

import personality as pr

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
attitude = Template(pr.rude)

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def sms_reply():
    number = request.form['From']
    body = request.form['Body']

    resp = MessagingResponse()
    resp.message(get_response(body))
    return Response(str(resp), mimetype="application/xml")

def get_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=attitude.substitute({'PROMPT': prompt}),
        max_tokens=300,
        temperature=0.5,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        stop=["You:"]
    )

    return response.choices[0].text


if __name__ == "__main__":
    app.run(debug=True)


# Board Game On a Hexagonal Board
# coordinates.py
class Coord(tuple):
    def __init__(self, pos):
        self._coord = pos
        self.s, self.q, self.r = pos

    def __iter__(self):
        yield from self._coord

    def __add__(self, val):
        return Coord(tuple(map(sum, zip(self._coord, val))))

    def __sub__(self, val):
        inverse_val = (x * -1 for x in val)
        return Coord(tuple(map(sum, zip(self._coord, val))))

    def __truediv__(self, target):
        sub = self.__sub__(target)
        return max(abs(sub.s), abs(sub.q), abs(sub.r))

    def __str__(self):
        return str(self._coord)

# hextiles.py
@dataclass
class HexTile:

    def __init__(self, coord):
        self.coord = Coord(coord)
        self.occupant = []
        self.lotus = []
        self.safe = self.coord not in Map.unsafe_tiles
        self.inBounds = self.coord in Map.tiles

    def __str__(self):
        return str(self.coord)

    def __repr__(self):
        return f"{self.__class__}: -->  {self.coord!r}\n{' ' * len(str(self.__class__))}  --> Occupant: {self.occupant}"

    @property
    def up(self):
        return tuple(self.coord + Coord(Rules.up))

    @property
    def upright(self):
        return tuple(self.coord + Coord(Rules.upright))

    @property
    def downright(self):
        return tuple(self.coord + Coord(Rules.downright))

    @property
    def down(self):
        return tuple(self.coord + Coord(Rules.down))

    @property
    def downleft(self):
        return tuple(self.coord + Coord(Rules.downleft))

    @property
    def upleft(self):
        return tuple(self.coord + Coord(Rules.upleft))

    @property
    def neighbors(self):
        return (
            self.up,
            self.upright,
            self.downright,
            self.down,
            self.downleft,
            self.upleft
        )


# pieces.py

Piece = namedtuple("Piece",["id", "range", "value", "type", "position", "active"])
Piece.__doc__ += ": Enso Koi Game Piece"
Piece.id.__doc__ = "Identifier of Game Piece"
Piece.range.__doc__ = "Maximum number of moveable spaces"
Piece.value.__doc__ = "Point value for captured Game Piece"
Piece.type.__doc__ = "Classification of Game Piece"
Piece.position.__doc__ = "Position of Game Piece on the Board"
Piece.active.__doc__ = "Game Piece is live on the board"

KoiPiece = namedtuple("Koi", Piece._fields + ("multi", "jumps", "canStone", "canLotus", "flipped"))
KoiPiece.__doc__ += ": Playable Koi Piece"
KoiPiece.multi.__doc__ = "Is Koi multi-directional: bool"
KoiPiece.jumps.__doc__ = "Maximum number of jumps: 1 | 2"
KoiPiece.canStone.__doc__ = "Is Koi able to jump stones: bool"
KoiPiece.canLotus.__doc__ = "Is Koi able to capture White Lotus: bool"
KoiPiece.flipped.__doc__ = "Is Koi in flipped position: bool"


    # Board Pieces
Stone       = lambda name: Piece(id=name, range=0, value=0.5, type="Stone", position=None, active=False)
White_Lotus = lambda name: Piece(id=name, range=0, value=5, type="WhiteLotus", position=None, active=False)
Tile_Lotus  = lambda name: Piece(id=name, range=0, value=0, type="Lotus", position=None, active=False)

    # Player Pieces
Tancho      = lambda name: KoiPiece(id=name, range=2, value=1, type="Koi", multi=False, jumps=2, canStone=False, canLotus=False, position=None, active=False, flipped=False)
Asagi       = lambda name: KoiPiece(id=name, range=3, value=1, type="Koi", multi=False, jumps=1, canStone=True, canLotus=False, position=None, active=False, flipped=False)
Kumonryu    = lambda name: KoiPiece(id=name, range=4, value=1, type="Koi", multi=False, jumps=1, canStone=False, canLotus=True, position=None, active=False, flipped=False)
Utsuri      = lambda name: KoiPiece(id=name, range=2, value=2, type="Koi", multi=True, jumps=2, canStone=False, canLotus=False, position=None, active=False, flipped=False)
Ogon        = lambda name: KoiPiece(id=name, range=3, value=2, type="Koi", multi=True, jumps=1, canStone=True, canLotus=False, position=None, active=False, flipped=False)
Sumi        = lambda name: KoiPiece(id=name, range=4, value=2, type="Koi", multi=True, jumps=1, canStone=False, canLotus=True, position=None, active=False, flipped=False)


# player.py

class InitialTeam:

    @property
    def koi(self):
        return (
            Tancho("TanchoA"),
            Tancho("TanchoB"),
            Tancho("TanchoC"),
            Tancho("TanchoD"),
            Asagi("AsagiA"),
            Asagi("AsagiB"),
            Kumonryu("KumonryuA"),
            Kumonryu("KumonryuB"),
            Utsuri("UtsuriA"),
            Utsuri("UtsuriB"),
            Ogon("OgonA"),
            Ogon("OgonB"),
            Sumi("Sumi"),
        )

    @property
    def stones(self):
        return (
            Stone("StoneA"),
            Stone("StoneB"),
            Stone("StoneC"),
            Stone("StoneD"),
            Stone("StoneE"),
        )

    @property
    def lotustiles(self):
        return (
            Tile_Lotus("LotusA"),
            Tile_Lotus("LotusB"),
            Tile_Lotus("LotusC"),
            Tile_Lotus("LotusD"),
            Tile_Lotus("LotusE"),
            Tile_Lotus("LotusF"),
            Tile_Lotus("LotusG"),
            Tile_Lotus("LotusH"),
            Tile_Lotus("LotusI"),
        )


class Player:

    def __init__(self, name=""):
        self._order = None
        self.player_name = name
        self.score = 0
        self.team = InitialTeam()
        self.captured = {}
        self.stones = []


# Barcode Scanner from Webcam

import cv2
from pyzbar import pyzbar

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    barcodes = pyzbar.decode(gray)

    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type

        print(f"Found {barcode_type} barcode: {barcode_data}")

    cv2.imshow("Barcode Scanner", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
