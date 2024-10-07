# 🚀 Illiterally Implementation
from typing import *
import dataclasses
import slugify
import jinja2
import emoji
import io
import os

from illiterally.log import Log, Indent
from illiterally.block import Block,BlockReader
from illiterally.state import State

# 🚀 Entry Point
def illiterally( source_files: list[str], template_files: list[str], block_template: str, output_dir: str='./output', source_prefix: Optional[str]=None, template_prefix: Optional[str]=None, left: str=None, right: str=None, source_url: str='', output_url: str='', suppress: bool=False ):
    S = State(
        source_files = source_files,
        template_files = template_files,
        block_template = block_template, 
        output_dir = output_dir,
        source_prefix = source_prefix,
        template_prefix = template_prefix,
        left = left,
        right = right,
        source_url = source_url,
        output_url = output_url,
        suppress = suppress
    )

    # build a list of all slugs in the source files
    blocks,duplicates = S.parse_blocks()
    if len(duplicates) > 0:
        # duplicates found, de-duplicate
        blocks,duplicates = S.parse_blocks(duplicates)
        if len(duplicates) > 0:
            # duplicates still found. What the...
            return 1

    # now go over all of the template files and activate
    # any blocks that they will render
    S.activate_blocks_from_templates( blocks )
    S.render_blocks_from_templates( blocks )

    return 0

# 🚗
# 🚗