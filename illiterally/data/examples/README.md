{% import 'macros.md.inc' as macros with context %}
illiterally 🔥
============== 

![Unit Tests](https://github.com/jamesgregson/illiterally/actions/workflows/unit-test.yml/badge.svg)

Welcome to 🔥, the simplest (il)literate programming tool ever envisioned. Rather than assembling your program from code fragments scattered through documentation like conventional [Literate Programming](https://en.wikipedia.org/wiki/Literate_programming), 🔥 generates documentation by extracting snippets bracketed by emojis from your code. Then it renders them into documentation templates with Jinja.

Snippets are defined simply by having a line containing 🔥. Everything that follows on that line defines the snippet name (except leading/trailing whitespace). All lines that follow become part of the snippet unit the next 🧯 line. Since almost every language has line-level comments, this allows 🔥 to handle just about anything without modifications.

***Why is this better?*** Classic Literate Programming builds your program from source code snippets embedded within documentation. It's conceptually elegant but difficult to integrate into modern development practices. In 🔥, your code is just ordinary code with some delimiting emojis. You can use it with [CMake](https://cmake.org/) and compile as usual. You can test it with [GoogleTest](https://github.com/google/googletest), launch it in a debugger, whatever. It's just code that has irritating emojis scattered everywhere. Then 🔥 uses it to produce documents with irritating emojis scattered everywhere. Awesome!

***Can we disable irritating emojis?*** 😬 Harsh question, you might be missing the point. But yes, you can provide any text strings or alternate emojis you want as begin and end tokens, as long as they won't appear in your code **and** that you can escape them properly. The ***catch*** is that it may be harder than you think to find delimiters that don't conflict with your target language and appear pleasing. So if you want to use [🫸 and 🫷](./docs/handmoji.md) or [`<<<:` and `:>>>`](./docs/nomoji.md)🤮 you can. 

# Features

Here's some key features of 🔥:

- **🔥 is simple:** The whole thing is around 200loc, generously. Want to change it? You definitely can.
- **🔥 is unopinionated:** 🔥 maps text to text. It doesn't really care what's in the text before or after as long as there's delimiters.
- **🔥 is unobtrusive:** It does not try to replace your work flow or tool chain. You just chuck some comments in your code.
- **🔥 has a CLI and API:** When installed via pip, 🔥 exposes a simple `illiterally` command that mirrors the one public API call.
- **🔥 has delimiter suppression:** Suppress ***all*** delimiters in output if you're feeling extra professional.
- **🔥 auto-detects delimiters:** If not specified, the first two distinct emojis in the file serve as block delimiters 
- **🔥 is as irritating as Jinja:** You probably messed up a template or slug. 

# Supported Formats

Really any reasonable text-based format can likely be supported, however there are currently samples for the following formats:

| Format | Example | Block Template | Output |
|--------|---------|----------------|--------|
| Markdown | [example](illiterally/data/examples/docs/example.md)   | [template](illiterally/data/blocks/block.md)   | [Output](./docs/example.md)   |
| HTML     | [example](illiterally/data/examples/docs/example.html) | [template](illiterally/data/blocks/block.html) | [Output](./docs/example.html) |
| Latex    | [example](illiterally/data/examples/docs/example.tex)  | [template](illiterally/data/blocks/block.tex)  | [Output](./docs/example.tex)  |


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

To use 🔥, you need annotated source files, output templates and a block template. Let's look at each using a basic C++ hello world example. To run this demo, move to an empty directory of your choice and run (with the venv active):

```bash
# this will set up the files seen above in your current directory
# and create a run.sh file that will generate the demo output
lit_demo
```

Then run `chmod +x run.sh && ./run.sh` (linux/os-x) or copy it's contents to a terminal with the venv active and run it. This should print something like the following:

```bash
 % chmod +x run.sh ; ./run.sh
Starting 🔥
  Building index:
    Processing file: /Users/james/Code/tmp/example.cpp, ../example.cpp
  Loading block template: /Users/james/Code/illiterally/illiterally/data/blocks/block.md
    Rendering block: maybe
    Rendering block: let-s-see
  Rendering output files... from /Users/james/Code/tmp
    Rendering file: /Users/james/Code/tmp/output/example.md
```

The results should be the same as [docs/example.md](./docs/example.md), except with paths slightly different. Now check out the `example.cpp` and `example.md` files in your directory:

The source files are simply regular code with 🔥 and 🧯 denoting the start and end of each snippet: 

**[example.cpp](./docs/example.cpp):**
`````cpp
{{ include_file('./docs/example.cpp') }}
`````
 
The output templates, markdown in this case, include references to the blocks using via their slug:

**[example.md](./docs/example.md):**
`````text
{{ include_file('./docs/example.md') }}
`````

The block template controls how each block is rendered to the file. 🔥 provides a set of basic templates for common text-based document formats but you can also define your own. Here's we'll use the built-in one for markdown [block.md](./illiterally/data/blocks/block.md) (note that you may want to look at the 'raw' file).

# Implementation

For an overview of how 🔥 works, check out [the implementation notes](./docs/implementation.md).