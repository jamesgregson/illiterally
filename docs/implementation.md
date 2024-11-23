
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

- [Entry Point](/Users/james/Code/illiterally/docs/implementation.md#entry-point)

___

The stuff above is a code block rendered with the provided markdown template. 🔥 highlights that this is a block and provides a link to the source file, then includes the block itself. Any nested blocks are condensed. It also provides a list of direct links to the nested links.

> Except for the code block itself, none of the above is done by 🔥. It's actually customized by the template, which provides links to the source file, sub-block links and breadcrumbs (See [Block Definition](/Users/james/Code/illiterally/docs/implementation.md#block-definition)) for lower block levels. Also the `utility-functions` bullet is not a link because the block hasn't been rendered anywhere in the output. The markdown template prints an error for blocks that are referenced but not rendered <font color="red">RefMissingBlock(utility-functions)</font> or that are referenced but don't exist at all <font color="red">RefInvalidSlug(missing-block)</font>.

## Main Entry Point

The main function for 🔥 is quite simple. It just reads the input files, parses out their block structures, then renders each into a text string. Finally it loads and renders out the output templates, providing the previously rendered blocks as an argument. That sounds like quite a bit, but it's only around 40loc: 

#### <a name="entry-point"></a>🚀**Entry Point**🚗: [../illiterally/illiterally.py: 14](../illiterally/illiterally.py)
___
```python
def illiterally( source_files: list[str], template_files: list[str], block_template: str, output_dir: str='./output', source_prefix: Optional[str]=None, template_prefix: Optional[str]=None, left: str=None, right: str=None, source_url: str='', output_url: str='', suppress: bool=False ):
    try: 
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
        if S.log.errors > 0:
            S.log.fatal('State initialization invalid, check log/arguments')

        # build a list of all slugs in the source files
        blocks,duplicates = S.parse_blocks()
        if len(duplicates) > 0:
            # duplicates found, de-duplicate
            blocks,duplicates = S.parse_blocks(duplicates)
            if len(duplicates) > 0:
                # duplicates still found. What the...
                S.log.fatal('Duplicate blocks found after de-duplication, should never happen.')

        # now go over all of the template files and activate
        # any blocks that they will render
        S.activate_blocks_from_templates( blocks )
        S.render_blocks_from_templates( blocks )
    except RuntimeError as err:
        return 2
    
    return 0 if S.log.errors == 0 else 1

```
<span>[Illiterally Implementation](/Users/james/Code/illiterally/docs/implementation.md#illiterally-implementation) |&nbsp;Entry Point</span>

___

## Block Structure

Blocks represent parsed snippets of the input and store their ancestor and descendants and path to the root, all referenced as slugs (see below). The hierarchy information allows navigation links and breadcrumbs between code snippets. The blocks also store information about the line they start at, the file they were produced from and the slug that will be used to reference them:

#### <a name="block-definition"></a>🚀**Block Definition**🚗: [../illiterally/block.py: 10](../illiterally/block.py)
___
```python
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

```


___

> With the markdown template, nested blocks provide back-links as ***breadcrumbs*** to access multiple levels of hierarchy quickly. 

The final field, `Block.rendered` contains the rendered text from the block template. Output templates can reference this with `blocks['block-slug'].rendered`, where `block-slug` is the ***sluggified*** version of the name provided at the start of the block.

## Block Parser

The parser is a simple recursive descent bracket matching parser.  

#### <a name="block-reader"></a>🚀**Block Reader**🚗: [../illiterally/block.py: 32](../illiterally/block.py)
___
```python
class BlockReader:

    # 🚀 Entry point for parsing 🚗

    # 🚀 Delimiter auto-detection 🚗

    # 🚀 Parser state 🚗

    # 🚀 Bracket Detection 🚗

    # 🚀 Block parsing 🚗

```

- [Entry point for parsing](/Users/james/Code/illiterally/docs/implementation.md#entry-point-for-parsing)
- [Parser state](/Users/james/Code/illiterally/docs/implementation.md#parser-state)
- [Bracket Detection](/Users/james/Code/illiterally/docs/implementation.md#bracket-detection)
- [Block parsing](/Users/james/Code/illiterally/docs/implementation.md#block-parsing)

___

The parser itself is a class simply to maintain the small amount of state needed to track blocks that are encountered, the state of the input file and so on:

#### <a name="parser-state"></a>🚀**Parser state**🚗: [../illiterally/block.py: 65](../illiterally/block.py)
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
<span>[Block Reader](/Users/james/Code/illiterally/docs/implementation.md#block-reader) |&nbsp;Parser state</span>

___

The `BlockParser` class should not be instantiated directly. Instead the entry point for the parser is the static method `BlockReader.index_blocks`:

#### <a name="entry-point-for-parsing"></a>🚀**Entry point for parsing**🚗: [../illiterally/block.py: 35](../illiterally/block.py)
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
<span>[Block Reader](/Users/james/Code/illiterally/docs/implementation.md#block-reader) |&nbsp;Entry point for parsing</span>

___

It just sets up a dummy block that will be discarded and starts the recursion. The recursion just reads lines and checks for opening/closing emojis. If none are present, the current line is appended to the open block (initially a dummy block). Whenever a closing emoji is found, the current block ends and the function returns. Whenever an opening emoji is found, the function recurses on a new block, setting up hierarchy references and suspending adding lines to the previous block until the new block is complete.

#### <a name="block-parsing"></a>🚀**Block parsing**🚗: [../illiterally/block.py: 94](../illiterally/block.py)
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
<span>[Block Reader](/Users/james/Code/illiterally/docs/implementation.md#block-reader) |&nbsp;Block parsing</span>

___

Bracket parsing is very simple, emojis are converted to a text representation and the input line is split with them. Content following open delimiters is stripped and forms a new snippet name:

#### <a name="bracket-detection"></a>🚀**Bracket Detection**🚗: [../illiterally/block.py: 84](../illiterally/block.py)
___
```python
    def is_left( self, line: str ) -> str:
        toks = emoji.demojize(line).split(self.left)
        return toks[1].strip() if len(toks) == 2 else None
    
    def is_right( self, line: str ) -> str:
        toks = emoji.demojize(line).split(self.right)
        return toks[1].strip() if len(toks) == 2 else None

```
<span>[Block Reader](/Users/james/Code/illiterally/docs/implementation.md#block-reader) |&nbsp;Bracket Detection</span>

___

That's illiterally it.