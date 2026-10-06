import re
import tomllib
from pathlib import Path

import genanki
import pygments.formatters
import pygments.lexers
from markdown_it import MarkdownIt

LAST_CHAPTER_NUM = 21
DECK_ID_PREFIX = "12592208"
CSS = pygments.formatters.HtmlFormatter(style="nord").get_style_defs("pre") + """
pre {
	padding: 0.5em 0.8em; /* add some padding between the code and the border */
	overflow-x: auto; /* add horizontal scroll if the code is too wide */
	tab-size: 4;
}
/* Anki's default */
.card {
	font-size: 20px;
	line-height: 1.5;
}
.cloze {
	font-weight: bold;
	color: blue;
}
.nightMode .cloze {
	color: lightblue;
}
"""
# noinspection SpellCheckingInspection
MODEL_BASIC = genanki.Model(model_id=1534339908,
                            name="Rust Book Basic",
                            fields=[{"name": "id"}, {"name": "front"}, {"name": "back"}],
                            templates=[{"name": "Card 1",
                                        "qfmt": "{{front}}",
                                        "afmt": "{{FrontSide}}<hr id='answer'>{{back}}"}],
                            css=CSS)
# noinspection SpellCheckingInspection
MODEL_CLOZE = genanki.Model(model_id=1220447748,
                            name="Rust Book Cloze",
                            fields=[{"name": "id"}, {"name": "text"}, {"name": "extra"}],
                            templates=[{"name": "Card 1",
                                        "qfmt": "{{cloze:text}}",
                                        "afmt": "{{cloze:text}}{{#extra}}<hr id='answer'>{{extra}}{{/extra}}"}],
                            css=CSS,
                            model_type=genanki.Model.CLOZE)


def generate_deck_id(chapter_num: int) -> int:
	return int(f"{DECK_ID_PREFIX}{chapter_num:02}")


def generate_deck_name(chapter_num: int) -> str:
	for line in Path("book/src/SUMMARY.md").read_text().splitlines():
		if f"ch{chapter_num:02}-00" in line and (m := re.search(r"(?<=\[)(.*?)(?=])", line)) is not None:
			# extract the chapter title between []
			return m[0]

	raise ValueError("Should not happen: chapter title not found in SUMMARY.md")


def parse_markdown(text: str) -> str:
	return md.render(text)


def parse_card(card: dict) -> genanki.Note:
	match card["type"]:
		case "basic":
			model = MODEL_BASIC
			fields = [card["id"], parse_markdown(card["front"]), parse_markdown(card["back"])]
		case "cloze":
			model = MODEL_CLOZE
			fields = [card["id"], parse_markdown(card["text"]), parse_markdown(card.get("extra", ""))]
		case _:
			raise ValueError(f"Unknown card type: {card["type"]}")

	tags = ["rust-book-deleted"] if card.get("deleted") else []
	guid = card["id"]

	# noinspection unbound-local-variable
	return genanki.Note(model=model, fields=fields, tags=tags, guid=guid)


def highlight_code(code: str, lang: str, _: str) -> str:
	# markdown-it-py will handle the wrapping of the code block
	return pygments.highlight(code, pygments.lexers.get_lexer_by_name(lang),
	                          pygments.formatters.HtmlFormatter(nowrap=True))


# Vec<T> will be rendered wrongly if HTML is enabled
# code syntax highlighting is passed to pygments
md = MarkdownIt(options_update={"html": False, "highlight": highlight_code})


def main():
	Path("dist").mkdir(exist_ok=True)
	decks = []

	for chapter_num in range(1, LAST_CHAPTER_NUM + 1):
		chapter_deck = genanki.Deck(deck_id=generate_deck_id(chapter_num),
		                            name=f"Rust Book::{chapter_num:02} {generate_deck_name(chapter_num)}")

		for card_file in Path("cards").glob(f"ch{chapter_num:02}-*.toml"):
			for card in tomllib.loads(card_file.read_text()).get("cards", []):
				chapter_deck.add_note(parse_card(card))

		decks.append(chapter_deck)
		genanki.Package(decks).write_to_file(f"dist/rust-book-upto-ch{chapter_num:02}.apkg")


if __name__ == "__main__":
	main()
