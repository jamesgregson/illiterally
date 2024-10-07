
illiterally 🔥
============== 

![Unit Tests](https://github.com/jamesgregson/illiterally/actions/workflows/unit-tests.yml/badge.svg)

Welcome to 🔥, the simplest (il)literate programming tool ever envisioned. Rather than assembling your program from code fragments scattered through documentation like conventional [Literate Programming](https://en.wikipedia.org/wiki/Literate_programming), 🔥 generates documentation by extracting snippets bracketed by emojis from your code. Then it renders them into documentation templates with Jinja.

Snippets are defined simply by having a line containing 🔥. Everything that follows on that line defines the snippet name (except leading/trailing whitespace). All lines that follow become part of the snippet unit the next 🧯 line. Since almost every language has line-level comments, this allows 🔥 to handle just about anything without modifications.

***Why is this better?*** Classic Literate Programming builds your program from source code snippets embedded within documentation. It's conceptually elegant but difficult to integrate into modern development practices. In 🔥, your code is just ordinary code with some delimiting emojis. You can use it with [CMake](https://cmake.org/) and compile as usual. You can test it with [GoogleTest](https://github.com/google/googletest), launch it in a debugger, whatever. It's just code that has irritating emojis scattered everywhere. Then 🔥 uses it to produce documents with irritating emojis scattered everywhere. Awesome!

***Can we disable irritating emojis?*** 😬 Harsh question, you might be missing the point. But yes, you can provide any text strings or alternate emojis you want as begin and end tokens, as long as they won't appear in your code **and** that you can escape them properly. The ***catch*** is that it may be harder than you think to find delimiters that don't conflict with your target language and appear pleasing. So if you want to use [🫸 and 🫷](./docs/handmoji.md) or [`<<<:` and `:>>>`](./docs/nomoji.md)🤮 you can. 

# Features

Here's some key features of 🔥:

- **🔥 is simple:** The whole thing is around 400loc, generously. Want to change it? You definitely can.
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

Choose one of the following:

```bash
# recommended initial virtual environment setup
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel

# then ONE of:

# (1) install illiterally from PyPI
pip install illiterally

# (2) from bleeding-edge 
pip install https://github.com/jamesgregson/illiterally.git

# (3) for development
git clone https://github.com/jamesgregson/illiterally.git
pip install -e ./illiterally
```

# Simple Demo

To use 🔥, you need annotated source files, output templates and a block template. Let's look at each using a basic C++ hello world example. To run this demo, move to an empty directory of your choice and run (with the venv active):

```bash
# this will set up the files seen above in your current directory
# and create a run.sh file that will generate the demo output
illiterally_demo
```

Then run `chmod +x run.sh && ./run.sh` (linux/os-x) or copy it's contents to a terminal with the venv active and run it. This should print something like the following:

```bash
 % chmod +x run.sh && ./run.sh
 Starting 🔥
  Building active slug index...
   Processing file: "/Users/james/Code/illiterally/tmp/example.cpp"...
    Found block at line 6: maybe = "Maybe".
    Found block at line 1: let-s-see = "Let's see".
  Activating blocks from templates...
   Template file: /Users/james/Code/illiterally/tmp/example.md...
    Activated slug let-s-see for template "/Users/james/Code/illiterally/tmp/output/example.md".
    Activated slug maybe for template "/Users/james/Code/illiterally/tmp/output/example.md".
  Rendering blocks from templates...
   Template file: /Users/james/Code/illiterally/tmp/example.md...
    Rendered block let-s-see for template "/Users/james/Code/illiterally/tmp/output/example.md".
    Rendered block maybe for template "/Users/james/Code/illiterally/tmp/output/example.md".
```

The results should be the same as [docs/example.md](./docs/example.md), except with paths slightly different. Now check out the `example.cpp` and `example.md` files in your directory:

The source files are simply regular code with 🔥 and 🧯 denoting the start and end of each snippet: 

**[example.cpp](./docs/example.cpp):**
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

**[example.md](./docs/example.md):**
`````text
{% import 'macros.md.inc' as macros with context %}
Hello World
===========

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

{{ macros.render('let-s-see') }}

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

{{ macros.render('maybe') }}

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. {{ macros.ref('let-s-see') }}.

`````

The block template controls how each block is rendered to the file. 🔥 provides a set of basic templates for common text-based document formats but you can also define your own. Here's we'll use the built-in one for markdown [block.md](./illiterally/data/blocks/block.md) (note that you may want to look at the 'raw' file).

# Implementation

For an overview of how 🔥 works, check out [the implementation notes](./docs/implementation.md).