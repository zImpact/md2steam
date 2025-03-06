import re
from typing import Tuple, List


def convert_code_spans(text: str) -> Tuple[str, List[str]]:
    """
    Finds inline code spans and replaces them with placeholders.
    Returns a tuple: (text with placeholders, list of code fragments found).
    """
    code_spans = []

    def code_span_repl(match: re.Match) -> str:
        code_content = match.group(1)
        code_spans.append(code_content)
        return f"@@CODE{len(code_spans)-1}@@"

    text = re.sub(r"`([^`]+?)`", code_span_repl, text)
    return text, code_spans


def restore_code_spans(text: str, code_spans: List[str]) -> str:
    """
    Restores previously saved code spans by replacing placeholders
    with [code]...[/code] tags.
    """
    for idx, code_content in enumerate(code_spans):
        text = text.replace(f"@@CODE{idx}@@", f"[code]{code_content}[/code]")
    return text


def convert_images(text: str) -> str:
    """
    Converts Markdown images of the form ![alt](URL) into [img]URL[/img].
    The title in quotes is ignored.
    """
    return re.sub(
        r'!\[.*?\]\(([^)\s"]+)(?:\s+"[^"]*")?\)', r"[img]\1[/img]", text
    )


def convert_links(text: str) -> str:
    """
    Converts Markdown links of the form [text](URL) into [url=URL]text[/url].
    The title in quotes is ignored.
    """

    def link_repl(match: re.Match) -> str:
        link_text = match.group(1)
        url = match.group(2)
        return f"[url={url}]{link_text}[/url]"

    return re.sub(r'\[([^]]+)\]\(([^)\s"]+)(?:\s+"[^"]*")?\)', link_repl, text)


def convert_bold(text: str) -> str:
    """
    Converts bold formatting.
    First handles bold+italic (triple markers), then bold (double markers).
    """
    text = re.sub(r"\*\*\*(.*?)\*\*\*", r"[b][i]\1[/i][/b]", text)
    text = re.sub(r"___(.*?)___", r"[b][i]\1[/i][/b]", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"[b]\1[/b]", text)
    text = re.sub(r"__(.*?)__", r"[b]\1[/b]", text)
    return text


def convert_italic(text: str) -> str:
    """
    Converts italic formatting.
    """
    text = re.sub(r"\*(.*?)\*", r"[i]\1[/i]", text)
    text = re.sub(r"_(.*?)_", r"[i]\1[/i]", text)
    return text


def convert_strike(text: str) -> str:
    """
    Converts strikethrough formatting.
    """
    return re.sub(r"~~(.*?)~~", r"[strike]\1[/strike]", text)


def convert_inline(text: str) -> str:
    """
    Main function to convert inline Markdown elements to Steam BBCode.
    Processes the text in stages:
      1. Protect inline code spans.
      2. Convert images.
      3. Convert links.
      4. Convert bold, italic, and strikethrough formatting.
      5. Restore inline code spans.
    """
    text, code_spans = convert_code_spans(text)
    text = convert_images(text)
    text = convert_links(text)
    text = convert_bold(text)
    text = convert_italic(text)
    text = convert_strike(text)
    text = restore_code_spans(text, code_spans)
    return text
