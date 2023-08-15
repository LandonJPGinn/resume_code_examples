import random
import textwrap
from pathlib import Path

import numpy as np
from CreatorPipeline.constants import DEFAULTS
import photoshop.api as ps
from PIL import Image, ImageFont

layouts = {
    "full_topic": {"txt": "center", "subject": "center", "topic": None},
    "full_subject": {"txt": "center", "subject": None, "topic": "center"},
    "full_text": {"txt": "center", "subject": None, "topic": None},
    "anchorman": {"txt": "left", "subject": "center", "topic": "right"},
    "anchorman_rev": {"txt": "right", "subject": "center", "topic": "left"},
    "flag": {"txt": "right", "subject": "left", "topic": "center"},
    "flag_rev": {"txt": "left", "subject": "right", "topic": "center"},
    "sidecar": {"txt": "left", "subject": "right", "topic": None},
    "sidecar_rev": {"txt": "right", "subject": "left", "topic": None},
}


class ThumbnailPSD:
    """Generates a thumbnail for the episode."""
    def __init__(self, outfile=None):
        self.outfile = DEFAULTS.thumbnail_output / DEFAULTS.research_thumb_psd
        print(self.outfile)
        if outfile:
            self.outfile = outfile

        self.ALL_FONTS = [
            str(x) for x in Path(DEFAULTS.thumbnail_fonts).iterdir() if x.is_file()
        ]
        self.ALL_BASE = [
            str(x)
            for x in Path(DEFAULTS.thumbnail_backgrounds).iterdir()
            if x.is_file()
        ]
        self.ALL_SUBJECTS = [
            str(x) for x in Path(DEFAULTS.thumbnail_subjects).iterdir() if x.is_file()
        ]
        self.ALL_TOPICS = [
            str(x) for x in Path(DEFAULTS.thumbnail_topics).iterdir() if x.is_file()
        ]
        self._get_layout()
        self._get_bg()
        print(self.__dict__)
        self.generate_thumbnail()

    def generate_thumbnail(self):
        """Generates the thumbnail."""
        print("dont error")
        # with Session(action="new_document") as self.ps:
        self.ps = ps.Application()
        print("//Beginning")
        for i in dir(self.ps):
            print(i)

        self.ps.preferences.rulerUnits = ps.Units.Pixels
        self.ps.displayDialogs = ps.DialogModes.DisplayNoDialogs
        self.doc = self.ps.documents.add()
        self.doc.resizeImage(self.width, self.height)
        self._import_bg()
        self._import_subject()
        self._import_topic()
        self._import_text()
        self.save()
        print("Thumbnail Generated")

    def _get_layout(self):
        """Selects a layout for the thumbnail."""
        self.width = 1456
        self.width_pad = int(self.width // 50)

        self.height = 816
        self.height_safe = self.height // 1.25
        self.height_pad = int(self.height // 33)
        layout = layouts.get(random.choice(list(layouts.keys())), None)
        if not layout:
            raise MissingLayoutError

        self.width_range = random.choice(range(7, 12))

        # x_shift = {
        #     "left": w_reg_1,
        #     "center": w_reg_2,
        #     "right": w_reg_3,
        # }

        self.thumb_text = layout["txt"]
        self.subj_align = layout["subject"]
        self.fg_align = layout["topic"]

    def _get_bg(self):
        """Selects a background for the thumbnail."""
        self.bg = random.choice(self.ALL_BASE)
        im = Image.open(self.bg).convert("RGB")
        img_array = np.array(im)
        avg_color = np.mean(img_array, axis=(0, 1))
        avg_color = np.uint8(avg_color)

        base_color = (255, 255, 255) if np.average(avg_color) < 85 else (0, 0, 0)

        self.fill_color = random.choice(
            [
                (255, 255, 0),
                base_color,
            ]
        )

    def save(self):
        """Saves the thumbnail."""
        if self.outfile:
            options = ps.PhotoshopSaveOptions()
            self.doc.saveAs(self.outfile, options, True)

    def _get_a_font(self):
        """Selects a font for the thumbnail."""
        try:
            selection = random.choice(self.ALL_FONTS)
            ImageFont.truetype(selection)
            return selection
        except OSError:
            return self._get_a_font()

    def _import_image(self, fpath):
        """Imports an image into the thumbnail."""
        desc = ps.ActionDescriptor
        idnull = self.ps.charIDToTypeID("null")
        print(idnull)
        print(fpath)
        print("try") # Not sure whats going on here. I cant get putPath to recognize self
        desc.putPath(idnull, fpath)
        print("try2")
        # event_id = self.ps.charIDToTypeID("Plc ")
        self.ps.executeAction(self.ps.charIDToTypeID("Plc "), desc)

    def _import_bg(self):
        """Imports the background into the thumbnail."""
        if self.bg:
            self._import_image(self.bg)

    def _import_subject(self):
        """Imports the subject into the thumbnail."""
        if self.subj_align:
            subj = random.choice(self.ALL_SUBJECTS)
            self._import_image(subj)

    def _import_topic(self):
        """Imports the topic into the thumbnail."""
        if self.fg_align:
            topic = random.choice(self.ALL_TOPICS)
            self._import_image(topic)

    def _import_text(self):
        """Imports the text into the thumbnail."""
        if not self.thumb_text:
            return
        lines = textwrap.wrap(self.thumb_text, width=self.width_range, break_long_words=False)
        line_count = len(lines)
        line_height = int((self.height_safe // line_count) // 1.4)
        line_spacing = int(line_height * 0.75)

        font_path = self._get_a_font()
        testfont = ImageFont.truetype(font_path, line_height)
        real_height = testfont.getbbox("A")[1]
        scale = int((line_height // real_height) * real_height)
        rot = random.choice(list(np.arange(0, 6, 0.1))) * -1

        new_text_layer = self.doc.artLayers.add()
        new_text_layer.name = "Thumb Text"
        new_text_layer.kind = ps.LayerKind.TextLayer
        new_text_layer.textItem.contents = "\r".join(lines)
        new_text_layer.textItem.useAutoLeading = False
        new_text_layer.textItem.leading = line_spacing
        new_text_layer.textItem.spaceAfter = line_spacing
        new_text_layer.textItem.position = [
            self.width_pad,
            self.height_pad,
        ]  # Todo: set this up with layout
        new_text_layer.textItem.size = scale
        new_text_layer.textItem.font = Path(font_path).stem
        text_color = ps.SolidColor()
        text_color.rgb.red = self.fill_color[0]
        text_color.rgb.green = self.fill_color[1]
        text_color.rgb.blue = self.fill_color[2]
        new_text_layer.textItem.color = text_color
        new_text_layer.rotate(rot)


class MissingLayoutError(Exception):
    """Raised when a layout is missing."""
    ...


"""

with Session(action="new_document") as self.ps:
    self.ps.app.preferences.rulerUnits = self.ps.Units.Pixels
    self.ps.app.displayDialogs = self.ps.DialogModes.DisplayNoDialogs
    self.doc = self.ps.app.documents.add()
    self.doc.resizeImage(self.width, self.height)
    self._import_bg()
    self._import_subject()
    self._import_topic()
    self._import_text()
    self.save()
"""