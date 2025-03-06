import re
from .inline_converter import convert_inline
from typing import List, Tuple


def markdown_to_steam_bbcode(markdown_text: str) -> str:
    """Converts text from Markdown format to Steam BBCode."""
    lines = markdown_text.splitlines()
    result_lines = []
    list_stack: List[Tuple[str, int]] = []
    current_quote_level = 0
    inside_code_block = False
    code_block_accumulator: List[str] = []

    for raw_line in lines:
        if inside_code_block:
            if raw_line.strip().startswith("```"):
                inside_code_block = False
                code_content = "\n".join(code_block_accumulator)
                result_lines.append(f"[code]{code_content}[/code]")
                code_block_accumulator.clear()
            else:
                code_block_accumulator.append(raw_line)
            continue

        if raw_line.strip().startswith("```"):
            inside_code_block = True
            code_block_accumulator.clear()
            continue

        if raw_line.strip() == "":
            while list_stack:
                list_type, _ = list_stack.pop()
                result_lines.append(
                    f"[/{'olist' if list_type == 'ol' else 'list'}]"
                )
            if current_quote_level > 0:
                result_lines.append("[/quote]" * current_quote_level)
                current_quote_level = 0
            result_lines.append("")
            continue

        leading_spaces = len(raw_line) - len(raw_line.lstrip(" "))
        first_char = raw_line.lstrip(" ")[:1]
        if list_stack:
            if not re.match(r"^\s*([-+*]|\d+\.)\s+", raw_line):
                is_quote_and_indented = (
                    first_char == ">" and leading_spaces > list_stack[-1][1]
                )
                if not is_quote_and_indented:
                    while list_stack:
                        list_type, _ = list_stack.pop()
                        result_lines.append(
                            f"[/{'olist' if list_type == 'ol' else 'list'}]"
                        )

        stripped_line = raw_line
        quote_depth = 0
        while stripped_line.startswith(">"):
            quote_depth += 1
            stripped_line = stripped_line[1:]
            if stripped_line.startswith(" "):
                stripped_line = stripped_line[1:]
        if quote_depth > 0:
            if quote_depth > current_quote_level:
                for _ in range(current_quote_level, quote_depth):
                    result_lines.append("[quote]")
            elif quote_depth < current_quote_level:
                for _ in range(quote_depth, current_quote_level):
                    result_lines.append("[/quote]")
            current_quote_level = quote_depth
        else:
            if current_quote_level > 0:
                result_lines.append("[/quote]" * current_quote_level)
                current_quote_level = 0

        line_content = stripped_line
        heading_match = re.match(r"^(#{1,6})\s+(.*)", line_content)
        if heading_match:
            level_markers = heading_match.group(1)
            heading_text = heading_match.group(2)
            level = len(level_markers)
            if level > 3:
                level = 3
            converted_heading = convert_inline(heading_text)
            result_lines.append(f"[h{level}]{converted_heading}[/h{level}]")
            continue

        if (
            re.match(r"^(-\s?){3,}$", line_content)
            or re.match(r"^(_\s?){3,}$", line_content)
            or re.match(r"^(\*\s?){3,}$", line_content)
        ):
            result_lines.append("[hr][/hr]")
            continue

        list_match = re.match(r"^(\s*)([-+*]|\d+\.)\s+(.*)", line_content)
        if list_match:
            indent_str = list_match.group(1)
            marker = list_match.group(2)
            item_text = list_match.group(3)
            indent_spaces = len(indent_str.expandtabs(4))
            list_type = "ol" if marker.rstrip(".").isdigit() else "ul"

            if not list_stack:
                list_stack.append((list_type, indent_spaces))
                result_lines.append(
                    "[olist]" if list_type == "ol" else "[list]"
                )
            else:
                if indent_spaces > list_stack[-1][1]:
                    list_stack.append((list_type, indent_spaces))
                    result_lines.append(
                        "[olist]" if list_type == "ol" else "[list]"
                    )
                elif indent_spaces < list_stack[-1][1]:
                    while list_stack and indent_spaces < list_stack[-1][1]:
                        prev_type, _ = list_stack.pop()
                        result_lines.append(
                            f"[/{'olist' if prev_type == 'ol' else 'list'}]"
                        )
                    if list_stack and list_stack[-1][1] == indent_spaces:
                        if list_stack[-1][0] != list_type:
                            prev_type, _ = list_stack.pop()
                            list_tag = "olist" if prev_type == "ol" else "list"
                            result_lines.append(f"[/{list_tag}]")
                            list_stack.append((list_type, indent_spaces))
                            result_lines.append(
                                "[olist]" if list_type == "ol" else "[list]"
                            )
                    else:
                        list_stack.append((list_type, indent_spaces))
                        result_lines.append(
                            "[olist]" if list_type == "ol" else "[list]"
                        )
                else:
                    if list_stack[-1][0] != list_type:
                        prev_type, _ = list_stack.pop()
                        result_lines.append(
                            f"[/{'olist' if prev_type == 'ol' else 'list'}]"
                        )
                        list_stack.append((list_type, indent_spaces))
                        result_lines.append(
                            "[olist]" if list_type == "ol" else "[list]"
                        )

            converted_item = convert_inline(item_text)
            result_lines.append(f"[*] {converted_item}")
            continue

        result_lines.append(convert_inline(line_content))

    if inside_code_block:
        code_content = "\n".join(code_block_accumulator)
        result_lines.append(f"[code]{code_content}[/code]")
    while list_stack:
        list_type, _ = list_stack.pop()
        result_lines.append(f"[/{'olist' if list_type == 'ol' else 'list'}]")
    if current_quote_level > 0:
        result_lines.append("[/quote]" * current_quote_level)
        current_quote_level = 0

    return "\n".join(result_lines)
