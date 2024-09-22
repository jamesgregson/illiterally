{% import 'macros.md.inc' as macros with context %}
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
{{ include_file('lit/data/examples/docs/example.cpp') }}
`````

The output templates, markdown in this case, include references to the blocks using via their slug:

**[example.md](./lit/data/examples/docs/example.md):**
`````text
{{ include_file('lit/data/examples/docs/example.md') }}
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

{{ render('lit-implementation') }}

The stuff above is a code block rendered with the provided markdown template. 🔥 highlights that this is a block and provides a link to the source file, then includes the block itself. Any nested blocks are condensed. It also provides a list of direct links to the nested links.

> Except for the code block itself, none of the above is done by 🔥. It's actually customized by the template, which provides links to the source file, sub-block links and breadcrumbs (See {{macros.ref('block-definition')}}) for lower block levels. Also the `utility-functions` bullet is not a link because the block hasn't been rendered anywhere in the output. The markdown template prints an error for blocks that are referenced but not rendered {{ macros.ref('utility-functions') }} or that are referenced but don't exist at all {{ macros.ref('missing-block') }}.

## Main Entry Point

The main function for 🔥 is quite simple. It just reads the input files, parses out their block structures, then renders each into a text string. Finally it loads and renders out the output templates, providing the previously rendered blocks as an argument. That sounds like quite a bit, but it's only around 40loc: 

{{ render('entry-point') }}

## Block Structure

Blocks represent parsed snippets of the input and store their ancestor and descendants and path to the root, all referenced as slugs (see below). The hierarchy information allows navigation links and breadcrumbs between code snippets. The blocks also store information about the line they start at, the file they were produced from and the slug that will be used to reference them:

{{ render('block-definition') }}

> With the markdown template, nested blocks provide back-links as ***breadcrumbs*** to access multiple levels of hierarchy quickly. 

The final field, `Block.rendered` contains the rendered text from the block template. Output templates can reference this with `blocks['block-slug'].rendered`, where `block-slug` is the ***sluggified*** version of the name provided at the start of the block.

## Block Parser

The parser is a simple recursive descent bracket matching parser.  

{{ render('block-reader') }}

The parser itself is a class simply to maintain the small amount of state needed to track blocks that are encountered, the state of the input file and so on:

{{ render('parser-state') }}

The `BlockParser` class should not be instantiated directly. Instead the entry point for the parser is the static method `BlockReader.index_blocks`:

{{ render('entry-point-for-parsing') }}

It just sets up a dummy block that will be discarded and starts the recursion. The recursion just reads lines and checks for opening/closing emojis. If none are present, the current line is appended to the open block (initially a dummy block). Whenever a closing emoji is found, the current block ends and the function returns. Whenever an opening emoji is found, the function recurses on a new block, setting up hierarchy references and suspending adding lines to the previous block until the new block is complete.

{{ render('block-parsing') }}

Bracket parsing is very simple, emojis are converted to a text representation and the input line is split with them. Content following open delimiters is stripped and forms a new snippet name:

{{ render('bracket-detection') }}


That's literally 🔥.