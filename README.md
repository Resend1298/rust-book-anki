# rust-book-anki

Anki decks for [The Rust Programming Language](https://doc.rust-lang.org/book/).

## Using the decks

Download a package from releases.
There is one package per chapter, named `rust-book-upto-<chXX>.apkg`, and each contains every card up to and including that chapter.
Pick the one that matches how far you have read, for example `rust-book-upto-ch04.apkg` after finishing chapter 4, and import it into Anki.

When you read further, import a later package.

Each chapter has its own subdeck, such as `Rust Book::04 Understanding Ownership`.

### Deleted cards

Anki never deletes notes on import, so cards removed from this project are kept and tagged `rust-book-deleted` instead.
After importing, search for `tag:rust-book-deleted` in the browser and delete the results.

## How the cards are made

1. An agent reads a section of the book and writes its cards.
2. A human reviews the cards.

Cards live in `cards/`, one TOML file per section of the book.

## Building

```shell
git clone --recurse-submodules https://github.com/Resend1298/rust-book-anki.git
cd rust-book-anki
uv run main.py
```

The packages are written to `dist/`.

## License

[MIT](LICENSE)

Cards may contain content from the book, which is dual-licensed under Apache-2.0 and MIT.
See [Apache-2.0](https://github.com/rust-lang/book/blob/main/LICENSE-APACHE) and [MIT](https://github.com/rust-lang/book/blob/main/LICENSE-MIT) for details.
