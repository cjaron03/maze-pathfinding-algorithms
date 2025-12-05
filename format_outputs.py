#!/usr/bin/env python3

from pathlib import Path

CHAR_MAP = {
    '#': '#',      # wall
    'x': ' ',      # explored/open space (was 'x')
    '*': '+',      # final path (was '*')
    '.': '.',
    'S': 'S',
    'G': 'G',
    'o': 'O',
}

LEGEND_LINES = [
    'Legend:',
    '# = wall',
    "space = explored/open space (was 'x')",
    "+ = solution path (was '*')",
    '. = existing dots',
    "O = special item (was 'o')",
    'S = start',
    'G = goal',
]

OUTPUT_SUFFIX = '-readable'


def strip_legend(lines: list[str]) -> list[str]: # remove leading legend block if present
    """Remove leading legend block if present."""
    if lines[: len(LEGEND_LINES)] == LEGEND_LINES:
        idx = len(LEGEND_LINES)
        while idx < len(lines) and not lines[idx].strip():
            idx += 1
        return lines[idx:]
    return lines # no legend block found


def format_line(line: str) -> str: # translate one maze line using CHAR_MAP
    """Translate one maze line using the character map."""
    return ''.join(CHAR_MAP.get(ch, ch) for ch in line)


def make_readable_text(raw_text: str) -> str: # convert raw text to readable format
    lines = strip_legend(raw_text.splitlines())
    formatted_lines = [format_line(line) for line in lines]
    legend_block = '\n'.join(LEGEND_LINES)
    return legend_block + '\n\n' + '\n'.join(formatted_lines) + '\n'


def rewrite(path: Path) -> bool: # rewrite file if needed, return True if changed
    original_text = path.read_text()
    readable_text = make_readable_text(original_text)
    if original_text != readable_text:
        path.write_text(readable_text)
        return True
    return False


def main() -> None: # main function to process files in outputs directory
    output_dir = Path('outputs')
    if not output_dir.exists():
        raise SystemExit('outputs directory not found')

    for txt_path in sorted(p for p in output_dir.glob('*.txt') if not p.stem.endswith(OUTPUT_SUFFIX)): # process non-duplicate files
        replaced = rewrite(txt_path)
        action = 'Replaced' if replaced else 'Already formatted'
        print(f"{action} {txt_path}") # log action

    for dup_path in sorted(output_dir.glob(f"*{OUTPUT_SUFFIX}.txt")): # handle duplicate files
        base_stem = dup_path.stem[:-len(OUTPUT_SUFFIX)]
        dest_path = dup_path.with_name(f"{base_stem}{dup_path.suffix}")
        if dest_path.exists():
            print(f"Removed duplicate {dup_path}") # if destination exists, just remove duplicate
        else:
            dest_path.write_text(make_readable_text(dup_path.read_text())) 
            print(f"Promoted {dup_path} to {dest_path}") # promote duplicate to main file
        dup_path.unlink()


if __name__ == '__main__': 
    main()
