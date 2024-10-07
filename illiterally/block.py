from typing import *
import dataclasses
import os
import urllib.parse


import emoji
import slugify

# 🚀 Block Definition
@dataclasses.dataclass
class Block:
    name:          str          # name of block as read from file
    filename:      str          # source file block was found in
    line:          int          # line number where block was found
    text:          str = ''     # contents of the block
    slug:          str = ''     # the (potentially de-duplicated) block slug
    slug_base:     str = ''     # the original slug before de-duplication
    left:          str = None   # left delimiter
    right:         str = None   # right delimiter
    rendered_into: str = None   # file this block was rendered into

    parent:    str = ''     # slug of the parent block
    nested:    list[str] = dataclasses.field(default_factory=list) # first level of nested blocks, by slug
    path:      list[str] = dataclasses.field(default_factory=list) # slug path from root to this block

    @property
    def is_rendered( self ) -> bool:
        return self.rendered_into is not None
# 🚗

# 🚀 Block Reader
class BlockReader:

    # 🚀 Entry point for parsing
    @staticmethod
    def index_blocks( filename: str, *args, duplicates: Set[str]=None, left: str=None, right:str=None, **kwargs ):
        if left is None or right is None:
            left,right = BlockReader.detect_left_right( filename )
            if None in [left,right]:
                return None

        dummy = Block('dummy','invalid',-1)
        reader = BlockReader( filename, *args, duplicates=duplicates, left=left, right=right, **kwargs )
        reader.read_block( dummy )
        return reader.blocks
    # 🚗

    # 🚀 Delimiter auto-detection
    @staticmethod
    def detect_left_right( filename: str ):
        left, right = None, None
        for line in open(filename).readlines():
            emojis = emoji.distinct_emoji_list(line)
            if len(emojis) > 0:
                assert( len(emojis) == 1 )
                if left is None:
                    left = emojis[0]
                elif right is None and emojis[0] != left:
                    right = emojis[0]
                    return left,right
        return None,None
    # 🚗

    # 🚀 Parser state
    def __init__( self, filename, duplicates: Set[str]=None, left: str='🔥', right: str='🧯', suppress: bool=False ):
        self.duplicates = duplicates or set()
        self.left_emo  = emoji.emojize(left)
        self.left_str  = emoji.demojize(left)
        self.right_emo = emoji.emojize(right)
        self.right_str = emoji.demojize(right)
        self.suppress  = suppress
        self.filename = filename
        self.file = open(filename)
        self.line_number = 0
        self.blocks = {}

    def readline( self ):
        line = self.file.readline()
        self.line_number += 1
        return line
    # 🚗

    # 🚀 Bracket Detection
    def is_left( self, line: str ) -> str:
        toks = emoji.demojize(line).split(self.left)
        return toks[1].strip() if len(toks) == 2 else None
    
    def is_right( self, line: str ) -> str:
        toks = emoji.demojize(line).split(self.right)
        return toks[1].strip() if len(toks) == 2 else None
    # 🚗

    # 🚀 Block parsing
    def read_block( self, block: Block ):
        block.line = self.line_number
        while True:
            orig_line = self.readline()
            line = emoji.demojize( orig_line )
            if line == '':
                break
            elif self.left_str in line:
                name = line.split(self.left_str)[1].strip()
                slug = slugify.slugify(name)
                slug_base = slug
                if slug in self.duplicates:
                    slug = slugify.slugify( os.path.basename(self.filename) + '-' + slug )
                newblock = Block(
                    filename  = self.filename,
                    name      = name,
                    line      = self.line_number,
                    slug      = slug,
                    slug_base = slug_base,
                    parent    = block.slug,
                    path      = block.path + [slug],
                    left      = self.left_emo if not self.suppress else '',
                    right     = self.right_emo if not self.suppress else ''
                )
                self.read_block( newblock )
                self.blocks[newblock.slug] = newblock
                block.nested.append( newblock.slug )

                if self.suppress:                      
                    out = line.rstrip().replace(self.left_str,'') + os.linesep
                else:
                    out = orig_line.rstrip() + ' ' + self.right_emo + os.linesep
                block.text += out
            elif self.right_str in line:
                return
            else:
                block.text += line
    # 🚗
# 🚗