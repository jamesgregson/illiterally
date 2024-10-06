
🔥 Inner Workings
=================

Here's an overview of how 🔥 works, generated with 🔥 itself. With the overall size of 🔥 being ~200 lines, this is kind of overkill but it does serve as an example of what can be done:

> You might be wondering why you see 🚀 and 🚗 in the snippets instead of 🔥 and 🧯. The reason is that 🔥 allows you to specify the emojis delimiting snippets. So for the 🔥 code itself, which references 🔥 and 🧯 as block delimiters by default, 🚀 and 🚗 are used instead. This allows 🔥 to run on itself to generate this documentation.

#### <a name="illiterally-implementation"></a>🚀**Illiterally Implementation**🚗: [../illiterally/illiterally.py: 1](../illiterally/illiterally.py)
___
```python
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

# 🚀 Entry Point 🚗


```

- [Entry Point](#entry-point)

___

The stuff above is a code block rendered with the provided markdown template. 🔥 highlights that this is a block and provides a link to the source file, then includes the block itself. Any nested blocks are condensed. It also provides a list of direct links to the nested links.

> Except for the code block itself, none of the above is done by 🔥. It's actually customized by the template, which provides links to the source file, sub-block links and breadcrumbs (See [Block Definition](#block-definition)) for lower block levels. Also the `utility-functions` bullet is not a link because the block hasn't been rendered anywhere in the output. The markdown template prints an error for blocks that are referenced but not rendered <font color="red">RefMissingBlock(utility-functions)</font> or that are referenced but don't exist at all <font color="red">RefInvalidSlug(missing-block)</font>.

## Main Entry Point

The main function for 🔥 is quite simple. It just reads the input files, parses out their block structures, then renders each into a text string. Finally it loads and renders out the output templates, providing the previously rendered blocks as an argument. That sounds like quite a bit, but it's only around 40loc: 

#### <a name="entry-point"></a>🚀**Entry Point**🚗: [../illiterally/illiterally.py: 14](../illiterally/illiterally.py)
___
```python
def illiterally( source_files: list[str], template_files: list[str], block_template: str, output_dir: str='./output', source_prefix: Optional[str]=None, template_prefix: Optional[str]=None, left: str=None, right: str=None, suppress: bool=False ):
    S = State(
        source_files = source_files,
        template_files = template_files,
        block_template = block_template, 
        output_dir = output_dir,
        source_prefix = source_prefix,
        template_prefix = template_prefix,
        left = left,
        right = right,
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


```
<span>[Illiterally Implementation](#illiterally-implementation) |&nbsp;Entry Point</span>

___

## Block Structure

Blocks represent parsed snippets of the input and store their ancestor and descendants and path to the root, all referenced as slugs (see below). The hierarchy information allows navigation links and breadcrumbs between code snippets. The blocks also store information about the line they start at, the file they were produced from and the slug that will be used to reference them:

#### <a name="block-definition"></a>🚀**Block Definition**🚗: [../illiterally/block.py: 9](../illiterally/block.py)
___
```python
@dataclasses.dataclass
class Block:
    name:      str
    filename:  str
    line:      int 
    text:      str = ''
    slug:      str = ''
    slug_base: str = ''
    parent:    str = ''
    nested:    list[str] = dataclasses.field(default_factory=list)
    path:      list[str] = dataclasses.field(default_factory=list)
    left:      str = None
    right:     str = None
    #rendered:      str = None
    rendered_into: str = None

    @property
    def is_rendered( self ):
        return self.rendered_into is not None

    def source_path( self, targ: str ):
        return os.path.relpath( self.filename, os.path.dirname(targ) )

    def ref(self, targ: str ):
        if self.rendered_into == targ:
            return ''
        return os.path.relpath( self.rendered_into, os.path.dirname(targ) ) if self.rendered_into else 'INVALID'

```


___

> With the markdown template, nested blocks provide back-links as ***breadcrumbs*** to access multiple levels of hierarchy quickly. 

The final field, `Block.rendered` contains the rendered text from the block template. Output templates can reference this with `blocks['block-slug'].rendered`, where `block-slug` is the ***sluggified*** version of the name provided at the start of the block.

## Block Parser

The parser is a simple recursive descent bracket matching parser.  

#### <a name="block-reader"></a>🚀**Block Reader**🚗: [../illiterally/block.py: 39](../illiterally/block.py)
___
```python
class BlockReader:

    # 🚀 Entry point for parsing 🚗

    # 🚀 Delimiter auto-detection 🚗

    # 🚀 Parser state 🚗

    # 🚀 Bracket Detection 🚗

    # 🚀 Block parsing 🚗

```

- [Entry point for parsing](#entry-point-for-parsing)
- [Parser state](#parser-state)
- [Bracket Detection](#bracket-detection)
- [Block parsing](#block-parsing)

___

The parser itself is a class simply to maintain the small amount of state needed to track blocks that are encountered, the state of the input file and so on:

#### <a name="parser-state"></a>🚀**Parser state**🚗: [../illiterally/block.py: 72](../illiterally/block.py)
___
```python
    def __init__( self, filename, duplicates: Set[str]=None, left: str=':fire:', right: str=':fire_extinguisher:', suppress: bool=False ):
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

```
<span>[Block Reader](#block-reader) |&nbsp;Parser state</span>

___

The `BlockParser` class should not be instantiated directly. Instead the entry point for the parser is the static method `BlockReader.index_blocks`:

#### <a name="entry-point-for-parsing"></a>🚀**Entry point for parsing**🚗: [../illiterally/block.py: 42](../illiterally/block.py)
___
```python
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

```
<span>[Block Reader](#block-reader) |&nbsp;Entry point for parsing</span>

___

It just sets up a dummy block that will be discarded and starts the recursion. The recursion just reads lines and checks for opening/closing emojis. If none are present, the current line is appended to the open block (initially a dummy block). Whenever a closing emoji is found, the current block ends and the function returns. Whenever an opening emoji is found, the function recurses on a new block, setting up hierarchy references and suspending adding lines to the previous block until the new block is complete.

#### <a name="block-parsing"></a>🚀**Block parsing**🚗: [../illiterally/block.py: 101](../illiterally/block.py)
___
```python
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

```
<span>[Block Reader](#block-reader) |&nbsp;Block parsing</span>

___

Bracket parsing is very simple, emojis are converted to a text representation and the input line is split with them. Content following open delimiters is stripped and forms a new snippet name:

#### <a name="bracket-detection"></a>🚀**Bracket Detection**🚗: [../illiterally/block.py: 91](../illiterally/block.py)
___
```python
    def is_left( self, line: str ) -> str:
        toks = emoji.demojize(line).split(self.left)
        return toks[1].strip() if len(toks) == 2 else None
    
    def is_right( self, line: str ) -> str:
        toks = emoji.demojize(line).split(self.right)
        return toks[1].strip() if len(toks) == 2 else None

```
<span>[Block Reader](#block-reader) |&nbsp;Bracket Detection</span>

___

That's illiterally it.