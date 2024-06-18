import random as rnd
from typing import Tuple
from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont
import json
from trdg.utils import get_text_width, get_text_height

# Thai Unicode reference: https://jrgraphix.net/r/Unicode/0E00-0E7F
TH_TONE_MARKS = [
    "0xe47",
    "0xe48",
    "0xe49",
    "0xe4a",
    "0xe4b",
    "0xe4c",
    "0xe4d",
    "0xe4e",
]
TH_UNDER_VOWELS = ["0xe38", "0xe39", "\0xe3A"]
TH_UPPER_VOWELS = ["0xe31", "0xe34", "0xe35", "0xe36", "0xe37"]


def loadJsonFile(filepath, verbose = True, print_dict = False):
	"""
	Load a json file 
	"""
	if verbose == True : print("Loading a dictionary to filepath",filepath,".........")
	dictionary = {}
	
	with open(filepath) as jsonFile:
		dictionary = json.load(jsonFile)
	
	if verbose == True : print("Loaded Successfully")
	if print_dict == True : print(json.dumps(dictionary,indent = 4))

	return dictionary

def generate(
    text: str,
    font: str,
    text_color: str,
    font_size: int,
    orientation: int,
    space_width: int,
    character_spacing: int,
    fit: bool,
    word_split: bool,
    stroke_width: int = 0,
    stroke_fill: str = "#282828",
) -> Tuple:

    if orientation == 0:
        return _generate_horizontal_text(
            text,
            font,
            text_color,
            font_size,
            space_width,
            character_spacing,
            fit,
            word_split,
            stroke_width,
            stroke_fill,
        )
    elif orientation == 1:
        return _generate_vertical_text(
            text,
            font,
            text_color,
            font_size,
            space_width,
            character_spacing,
            fit,
            stroke_width,
            stroke_fill,
        )
    else:
        raise ValueError("Unknown orientation " + str(orientation))

def _compute_character_width(image_font: ImageFont, character: str) -> int:
    if len(character) == 1 and (
        "{0:#x}".format(ord(character))
        in TH_TONE_MARKS + TH_UNDER_VOWELS + TH_UNDER_VOWELS + TH_UPPER_VOWELS
    ):
        return 0
    # Casting as int to preserve the old behavior
    return round(image_font.getlength(character))


def _generate_horizontal_text(
    text: str,
    font: str,
    text_color: str,
    font_size: int,
    space_width: int,
    character_spacing: int,
    fit: bool,
    word_split: bool,
    stroke_width: int = 0,
    stroke_fill: str = "#282828",
) -> Tuple:

    fills = []
    if ".json" in text_color:
        text_color_file = loadJsonFile(text_color)
        for letter_no in range(len(text)):
            fills.append(text_color_file[str(letter_no)])
    else:
        for letter_no in range(len(text)):
            fills.append(text_color)    

    # fonts = []
    # if ".json" in font:
    #     font_file = loadJsonFile(font)
    #     for letter_no in range(len(text)):
    #         fonts.append(font_file[str(letter_no)])
    # else:   
    #     for letter_no in range(len(text)):
    #         fonts.append(text_color)   

    # fonts_paths = {
    # "0" : "/home/ndiwan2/projects/adversarial_logo/font_generation/fonts/google-open-source-fonts/convergence/Convergence-Regular.ttf",
    # "1" : "/home/ndiwan2/projects/adversarial_logo/font_generation/fonts/custom-fonts/yahoo-font/Yahoo.ttf",
    # "2" : "/home/ndiwan2/projects/adversarial_logo/font_generation/fonts/custom-fonts/product-sans/Product Sans Bold Italic.ttf",
    # "3" : "/home/ndiwan2/projects/adversarial_logo/font_generation/fonts/custom-fonts/yahoo-font/Yahoo.ttf",
    # "4" : "/home/ndiwan2/projects/adversarial_logo/font_generation/fonts/custom-fonts/yahoo-font/Yahoo.ttf",
    # "5" : "/home/ndiwan2/projects/adversarial_logo/font_generation/fonts/custom-fonts/yahoo-font/Yahoo.ttf"
    # }

    fonts_paths = {}
    
    if ".json" in font:
        fonts_paths = loadJsonFile(font)
    else:   
        for letter_no in range(len(text)):
            fonts_paths[str(letter_no)] = font

    image_fonts = [ImageFont.truetype(font=fonts_paths[str(font_no)], size=font_size) for font_no in fonts_paths]

    max_width = 0 
    for font_no in range(len(image_fonts)):
        max_width = max(max_width, int(get_text_width(image_fonts[font_no], " ") * space_width))

    space_width = max_width

    if word_split:
        splitted_text = []
        for w in text.split(" "):
            for w1 in w.split(" "):
                splitted_text.append(w1)
            splitted_text.append(" ")
        splitted_text.pop()
    else:
        splitted_text = text
    print("splitted text is ", splitted_text)
    
    piece_widths = [
        _compute_character_width(image_fonts[i_no], p) if p != " " else space_width
        for i_no, p in enumerate(splitted_text)
    ]

    text_width = sum(piece_widths)

    if not word_split:
        text_width += character_spacing * (len(text) - 1)

    # text_height = max([get_text_height(image_fonts, p) for p in splitted_text])

    max_height = 0 
    for font_no in range(len(image_fonts)):
        max_height  = max(max_height , max([get_text_height(image_fonts[font_no], p) for p in splitted_text]))
    
    text_height = max_height

    txt_img = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
    txt_mask = Image.new("RGB", (text_width, text_height), (0, 0, 0))

    txt_img_draw = ImageDraw.Draw(txt_img)
    txt_mask_draw = ImageDraw.Draw(txt_mask, mode="RGB")
    txt_mask_draw.fontmode = "1"

    # colors = [ImageColor.getrgb(c) for c in text_color.split(",")]
    # c1, c2 = colors[0], colors[-1]

    # fill = (
    #     rnd.randint(min(c1[0], c2[0]), max(c1[0], c2[0])),
    #     rnd.randint(min(c1[1], c2[1]), max(c1[1], c2[1])),
    #     rnd.randint(min(c1[2], c2[2]), max(c1[2], c2[2])),
    # )

    stroke_colors = [ImageColor.getrgb(c) for c in stroke_fill.split(",")]
    stroke_c1, stroke_c2 = stroke_colors[0], stroke_colors[-1]

    stroke_fill = (
        rnd.randint(min(stroke_c1[0], stroke_c2[0]), max(stroke_c1[0], stroke_c2[0])),
        rnd.randint(min(stroke_c1[1], stroke_c2[1]), max(stroke_c1[1], stroke_c2[1])),
        rnd.randint(min(stroke_c1[2], stroke_c2[2]), max(stroke_c1[2], stroke_c2[2])),
    )

    import sys
    print("Splitted Text = ", splitted_text)

    for i, p in enumerate(splitted_text):
        print("i is ", i)
        print("p is ", p)
        fill = fills[i]
        print("Fill = ", fill)

        txt_img_draw.text(
            (sum(piece_widths[0:i]) + i * character_spacing * int(not word_split), 0),
            p,
            fill=fill,
            font=image_fonts[i],
            stroke_width=stroke_width,
            stroke_fill=stroke_fill,
        )
        txt_mask_draw.text(
            (sum(piece_widths[0:i]) + i * character_spacing * int(not word_split), 0),
            p,
            fill=((i + 1) // (255 * 255), (i + 1) // 255, (i + 1) % 255),
            font=image_fonts[i],
            stroke_width=stroke_width,
            stroke_fill=stroke_fill,
        )

    if fit:
        return txt_img.crop(txt_img.getbbox()), txt_mask.crop(txt_img.getbbox())
    else:
        return txt_img, txt_mask


def _generate_vertical_text(
    text: str,
    font: str,
    text_color: str,
    font_size: int,
    space_width: int,
    character_spacing: int,
    fit: bool,
    stroke_width: int = 0,
    stroke_fill: str = "#282828",
) -> Tuple:
    image_font = ImageFont.truetype(font=font, size=font_size)

    space_height = int(get_text_height(image_font, " ") * space_width)

    char_heights = [
        get_text_height(image_font, c) if c != " " else space_height for c in text
    ]

    text_width = max([get_text_width(image_font, c) for c in text])
    text_height = sum(char_heights) + character_spacing * len(text)

    txt_img = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
    txt_mask = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))

    txt_img_draw = ImageDraw.Draw(txt_img)
    txt_mask_draw = ImageDraw.Draw(txt_mask)
    txt_mask_draw.fontmode = "1"

    colors = [ImageColor.getrgb(c) for c in text_color.split(",")]
    c1, c2 = colors[0], colors[-1]

    fill = (
        rnd.randint(c1[0], c2[0]),
        rnd.randint(c1[1], c2[1]),
        rnd.randint(c1[2], c2[2]),
    )

    stroke_colors = [ImageColor.getrgb(c) for c in stroke_fill.split(",")]
    stroke_c1, stroke_c2 = stroke_colors[0], stroke_colors[-1]

    stroke_fill = (
        rnd.randint(stroke_c1[0], stroke_c2[0]),
        rnd.randint(stroke_c1[1], stroke_c2[1]),
        rnd.randint(stroke_c1[2], stroke_c2[2]),
    )

    for i, c in enumerate(text):
        txt_img_draw.text(
            (0, sum(char_heights[0:i]) + i * character_spacing),
            c,
            fill=fill,
            font=image_font,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill,
        )
        txt_mask_draw.text(
            (0, sum(char_heights[0:i]) + i * character_spacing),
            c,
            fill=((i + 1) // (255 * 255), (i + 1) // 255, (i + 1) % 255),
            font=image_font,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill,
        )

    if fit:
        return txt_img.crop(txt_img.getbbox()), txt_mask.crop(txt_img.getbbox())
    else:
        return txt_img, txt_mask