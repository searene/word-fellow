from vocab_builder.domain.word.WordValueObject import WordContext


def convert_word_context_to_html(context: WordContext) -> str:
    return f"{context.get_prefix()}<b><u>{context.word}</u></b>{context.get_suffix()}"
