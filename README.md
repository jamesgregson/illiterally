
illiterally 🔥
============

Welcome to 🔥, the simplest (il)literate programming tool ever envisioned. Rather than assembling your program from code fragments scattered through documentation like conventional [Literate Programming](https://en.wikipedia.org/wiki/Literate_programming), 🔥 generates documentation by extracting snippets bracketed by emojis from your code. Then it renders them into documentation templates with Jinja.

Snippets are defined simply by having a line containing 🔥. Everything that follows on that line defines the snippet name (except leading/trailing whitespace). All lines that follow become part of the snippet unit the next 🧯 line. Since almost every language has line-level comments, this allows 🔥 to handle just about anything without modifications.

***Why is this better?*** Classic Literate Programming builds your program from source code snippets embedded within documentation. It's conceptually elegant but difficult to integrate into modern development practices. In 🔥, your code is just ordinary code with some delimiting emojis. You can use it with [CMake](https://cmake.org/) and compile as usual. You can test it with [GoogleTest](https://github.com/google/googletest), launch it in a debugger, whatever. It's just code that has irritating emojis scattered everywhere. Then 🔥 uses it to produce documents with irritating emojis scattered everywhere. Awesome!

***Can we disable irritating emojis?*** 😬 Harsh question, you might be missing the point. But yes, you can provide any text strings or alternate emojis you want as begin and end tokens, as long as they won't appear in your code **and** that you can escape them properly. The ***catch*** is that it may be harder than you think to find delimiters that don't conflict with your target language and appear pleasing. So if you want to use [🫸 and 🫷](./docs/handmoji.md) or [`<<<:` and `:>>>`](./docs/nomoji.md)🤮 you can. 

# Features

Here's some key features of 🔥:

- **🔥 is simple:** The whole thing is around 200loc, generously. Want to change it? You definitely can.
- **🔥 is unopinionated:** 🔥 maps text to text. It doesn't really care what's in the text before or after as long as there's delimiters.
- **🔥 is unobtrusive:** It does not try to replace your work flow or tool chain. You just chuck some comments in your code.
- **🔥 has a CLI and API:** When installed via pip, 🔥 exposes a simple `lit` command that mirrors the single `lit.lit` API call.
- **🔥 has delimiter suppression:** Suppress ***all*** delimiters in output if you're feeling extra professional.
- **🔥 auto-detects delimiters:** If not specified, the first two distinct emojis in the file serve as block delimiters 
- **🔥 is as irritating as Jinja:** You probably messed up a template or slug. 

# Setup

Clone and run the following [(venv highly recommended)](https://docs.python.org/3/library/venv.html) from the repository directory:

```bash
# initial os-x, linux venv setup
python3 -m venv venv
source venv/bin/activate

# install the repo editable
pip install -e .
```

# Basic Usage

To use 🔥, you need annotated source files, output templates and a block template. Let's look at each using a basic C++ hello world example.

The source files are simply regular code with 🔥 and 🧯 denoting the start and end of each snippet: 

**[example.cpp](./lit/data/examples/docs/example.cpp):**
`````cpp
//🔥 Let's see
#include <iostream>

int main( int argc, char **argv ){

    //🔥 Maybe
    std::cout << "Hello world." << std::endl;
    //🧯

    return 0;
}
//🧯
`````

The output templates, markdown in this case, include references to the blocks using via their slug:

**[example.md](./lit/data/examples/docs/example.md):**
`````text
{% import 'macros.md.inc' as macros with context %}
Hello World
===========

Let's give this a try:

{{ render('let-s-see') }}

I guess it works:

{{ render('maybe') }}

Here's a reference to the top level {{ macros.ref('let-s-see') }}.

`````

The block template controls how each block is rendered to the file. 🔥 provides a set of basic templates for common text-based document formats but you can also define your own. Here's we'll use the built-in one for markdown [block.md](./lit/data/blocks/block.md) (note that you may want to look at the 'raw' file).

To run this demo, move to an empty directory of your choice and run (with the venv active):

```bash
# this will set up the files seen above in your current directory
# and create a run.sh file that will generate the demo output
lit_demo
```

Then run `chmod +x run.sh && ./run.sh` (after checking its contents, of course). This should print something like the following:

```bash
Starting 🔥
  Building index:
    Processing file: /Users/james/Code/lit/tmp/example.cpp, ../example.cpp
  Loading block template: /Users/james/Code/lit/lit/data/blocks/block.md
    Rendering block: maybe
    Rendering block: let-s-see
  Rendering output files... from /Users/james/Code/lit/tmp
    Rendering file: /Users/james/Code/lit/tmp/output/example.md
```


# 🔥 Inner Workings

Here's an overview of how 🔥 works, generated with 🔥 itself. With the overall size of 🔥 being ~200 lines, this is kind of overkill but it does serve as an example of what can be done:

> You might be wondering why you see 🚀 and 🚗 in the snippets instead of 🔥 and 🧯. The reason is that 🔥 allows you to specify the emojis delimiting snippets. So for the 🔥 code itself, which references 🔥 and 🧯 as block delimiters by default, 🚀 and 🚗 are used instead. This allows 🔥 to run on itself to generate this documentation.

#### <a name="lit-implementation"></a>🚀**Lit Implementation**🚗: [lit/lit.py: 1](lit/lit.py)
___
```python
import dataclasses
import slugify
import jinja2
import emoji
import io
import os

# 🚀 Utility functions 🚗

# 🚀 Block Definition 🚗

# 🚀 Block Reader 🚗

# 🚀 Entry-point 🚗

```



- Utility functions

- [Block Definition](#block-definition)

- [Block Reader](#block-reader)

- [Entry-point](#entry-point)

___

The stuff above is a code block rendered with the provided markdown template. 🔥 highlights that this is a block and provides a link to the source file, then includes the block itself. Any nested blocks are condensed. It also provides a list of direct links to the nested links.

> Except for the code block itself, none of the above is done by 🔥. It's actually customized by the template, which provides links to the source file, sub-block links and breadcrumbs (See [Block Definition](/Users/james/Code/lit/README.md#block-definition)) for lower block levels. Also the `utility-functions` bullet is not a link because the block hasn't been rendered anywhere in the output. The markdown template prints an error for blocks that are referenced but not rendered <font color="red">MissingBlock(utility-functions)</font> or that are referenced but don't exist at all <font color="red">InvalidSlug(missing-block)</font>.

## Main Entry Point

The main function for 🔥 is quite simple. It just reads the input files, parses out their block structures, then renders each into a text string. Finally it loads and renders out the output templates, providing the previously rendered blocks as an argument. That sounds like quite a bit, but it's only around 40loc: 

#### <a name="entry-point"></a>🚀**Entry-point**🚗: [lit/lit.py: 150](lit/lit.py)
___
```python
def lit( source_files: list[str], block_template: list[str], output_files: list[str], left=None, right=None, source_prefix: str='.', output_prefix: str='.', output_dir: str='./output', suppress: bool=False ):
    block_template = block_template if os.path.exists(block_template) else data_file('blocks',block_template)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader([os.path.dirname(os.path.abspath(block_template)),data_file('blocks')]))

    # index all of the source files
    print('Starting :fire:')
    blocks = {}
    out_to_src_path = os.path.relpath( os.path.abspath(source_prefix), os.path.abspath(output_dir) )
    print('  Building index:')
    for source_file in source_files:
        rel_path = os.path.join( out_to_src_path, os.path.relpath(source_file,source_prefix)) 
        print(f'    Processing file: {os.path.abspath(source_file)}, {rel_path}')
        file_blocks = BlockReader.index_blocks( source_file, left=left, right=right, suppress=suppress )
        for key,blk in file_blocks.items():
            if key in blocks: print(f'      WARNING: Block "{key}" already exists, skipping.')
            else: blocks[key] = blk

    # first pass over the output templates to flag which blocks get rendered by the output templates
    for template_file in output_files:
        out_file = os.path.abspath( os.path.join( output_dir, os.path.relpath(template_file,output_prefix) ) )
        template = env.from_string( open(template_file).read() )
        template.render( blocks=blocks, block = lambda x: None, render=lambda x: blocks[x].activate(out_file), include_file=lambda x: x )

    # load the block template and render each block, giving access to the set of all blocks for breadcrumbs/hierarchy
    print(f'  Loading block template: {block_template}')
    blk_template = env.from_string( open(block_template).read() )
    for slug,block in blocks.items():
        print(f'    Rendering block: {slug}')
        block.rendered = blk_template.render(block=block,blocks=blocks,suppress=suppress)

    # Second pass to process all of the output templates and resolve the lit/lit.py variable
    print(f'  Rendering output files... from {os.getcwd()}')
    for template_file in output_files:
        out_file = os.path.abspath( os.path.join( output_dir, os.path.relpath(template_file,output_prefix) ) )
        os.makedirs( os.path.dirname( out_file ), exist_ok=True )
        print(f'    Rendering file: {os.path.abspath(out_file)}')
        template = env.from_string( open(template_file).read() )
        with open( out_file, 'w' ) as outf:
            outf.write( template.render(
                block=lambda x: blocks[x] if x in blocks else None,
                render=lambda x: blocks[x].render(out_file),
                include_file=lambda x: read_file(source_prefix,x),
            ))

```

<span>[Lit Implementation](#lit-implementation) | Entry-point</span>

___

## Block Structure

Blocks represent parsed snippets of the input and store their ancestor and descendants and path to the root, all referenced as slugs (see below). The hierarchy information allows navigation links and breadcrumbs between code snippets. The blocks also store information about the line they start at, the file they were produced from and the slug that will be used to reference them:

#### <a name="block-definition"></a>🚀**Block Definition**🚗: [lit/lit.py: 21](lit/lit.py)
___
```python
@dataclasses.dataclass
class Block:
    name:     str
    filename: str
    line:     int 
    text:     str = ''
    slug:     str = ''
    parent:   str = ''
    nested:   list[str] = dataclasses.field(default_factory=list)
    path:     list[str] = dataclasses.field(default_factory=list)
    left:     str = None
    right:    str = None
    rendered:      str|None = None
    rendered_into: str|None = None

    @property
    def is_rendered( self ):
        return self.rendered_into is not None

    def activate(self,into:str):
        assert self.rendered_into in [None,into]
        self.rendered_into = os.path.abspath(into)
        return ''

    def render(self,into: str):
        assert self.rendered_into in [None,into]
        return self.rendered.replace( 'lit/lit.py',os.path.relpath(self.filename,os.path.dirname(self.rendered_into)))
    

```

<span>[Lit Implementation](#lit-implementation) | Block Definition</span>

___

> With the markdown template, nested blocks provide back-links as ***breadcrumbs*** to access multiple levels of hierarchy quickly. 

The final field, `Block.rendered` contains the rendered text from the block template. Output templates can reference this with `blocks['block-slug'].rendered`, where `block-slug` is the ***sluggified*** version of the name provided at the start of the block.

## Block Parser

The parser is a simple recursive descent bracket matching parser.  

#### <a name="block-reader"></a>🚀**Block Reader**🚗: [lit/lit.py: 52](lit/lit.py)
___
```python
class BlockReader:

    # 🚀 Entry point for parsing 🚗

    # 🚀 Delimiter auto-detection 🚗

    # 🚀 Parser state 🚗

    # 🚀 Bracket Detection 🚗

    # 🚀 Block parsing 🚗

```

<span>[Lit Implementation](#lit-implementation) | Block Reader</span>

- [Entry point for parsing](#entry-point-for-parsing)

- Delimiter auto-detection

- [Parser state](#parser-state)

- [Bracket Detection](#bracket-detection)

- [Block parsing](#block-parsing)

___

The parser itself is a class simply to maintain the small amount of state needed to track blocks that are encountered, the state of the input file and so on:

#### <a name="parser-state"></a>🚀**Parser state**🚗: [lit/lit.py: 85](lit/lit.py)
___
```python
    def __init__( self, filename, left: str=':fire:', right: str=':fire_extinguisher:', suppress: bool=False ):
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

<span>[Lit Implementation](#lit-implementation) | [Block Reader](#block-reader) | Parser state</span>

___

The `BlockParser` class should not be instantiated directly. Instead the entry point for the parser is the static method `BlockReader.index_blocks`:

#### <a name="entry-point-for-parsing"></a>🚀**Entry point for parsing**🚗: [lit/lit.py: 55](lit/lit.py)
___
```python
    @staticmethod
    def index_blocks( filename: str, *args, left: str=None, right:str=None, **kwargs ):
        if left is None or right is None:
            left,right = BlockReader.detect_left_right( filename )
            if None in [left,right]:
                raise RuntimeWarning(f'Error parsing: {filename}, autodetection of delimiters failed.')

        dummy = Block('dummy','invalid',-1)
        reader = BlockReader( filename, *args, left=left, right=right, **kwargs )
        reader.read_block( dummy )
        return reader.blocks

```

<span>[Lit Implementation](#lit-implementation) | [Block Reader](#block-reader) | Entry point for parsing</span>

___

It just sets up a dummy block that will be discarded and starts the recursion. The recursion just reads lines and checks for opening/closing emojis. If none are present, the current line is appended to the open block (initially a dummy block). Whenever a closing emoji is found, the current block ends and the function returns. Whenever an opening emoji is found, the function recurses on a new block, setting up hierarchy references and suspending adding lines to the previous block until the new block is complete.

#### <a name="block-parsing"></a>🚀**Block parsing**🚗: [lit/lit.py: 113](lit/lit.py)
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
                newblock = Block(
                    filename = self.filename,
                    name     = name,
                    line     = self.line_number,
                    slug     = slug,
                    parent   = block.slug,
                    path     = block.path + [slug],
                    left     = self.left_emo if not self.suppress else '',
                    right    = self.right_emo if not self.suppress else ''
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

<span>[Lit Implementation](#lit-implementation) | [Block Reader](#block-reader) | Block parsing</span>

___

Bracket parsing is very simple, emojis are converted to a text representation and the input line is split with them. Content following open delimiters is stripped and forms a new snippet name:

#### <a name="bracket-detection"></a>🚀**Bracket Detection**🚗: [lit/lit.py: 103](lit/lit.py)
___
```python
    def is_left( self, line: str ) -> str | None:
        toks = emoji.demojize(line).split(self.left)
        return toks[1].strip() if len(toks) == 2 else None
    
    def is_right( self, line: str ) -> str | None:
        toks = emoji.demojize(line).split(self.right)
        return toks[1].strip() if len(toks) == 2 else None

```

<span>[Lit Implementation](#lit-implementation) | [Block Reader](#block-reader) | Bracket Detection</span>

___


That's literally 🔥.