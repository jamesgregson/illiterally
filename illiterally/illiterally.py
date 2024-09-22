# 🚀 Lit Implementation
import dataclasses
import slugify
import jinja2
import emoji
import io
import os

# 🚀 Utility functions
def root_dir(): 
    return os.path.dirname( __file__ ) 

def data_file( *args ): 
    return os.path.join( root_dir(), 'data', *args )

def read_file( prefix, file ):
    fname = os.path.join( prefix, file )
    return open( fname ).read()
# 🚗

# 🚀 Block Definition
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
        return self.rendered.replace( '{{SRC_PATH}}',os.path.relpath(self.filename,os.path.dirname(self.rendered_into)))
    
# 🚗

# 🚀 Block Reader
class BlockReader:

    # 🚀 Entry point for parsing
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
    def __init__( self, filename, left: str='🔥', right: str='🧯', suppress: bool=False ):
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
    def is_left( self, line: str ) -> str | None:
        toks = emoji.demojize(line).split(self.left)
        return toks[1].strip() if len(toks) == 2 else None
    
    def is_right( self, line: str ) -> str | None:
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
    # 🚗
# 🚗

# 🚀 Entry-point
def illiterally( source_files: list[str], block_template: list[str], output_files: list[str], left=None, right=None, source_prefix: str='.', output_prefix: str='.', output_dir: str='./output', suppress: bool=False ):
    block_template = block_template if os.path.exists(block_template) else data_file('blocks',block_template)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader([os.path.dirname(os.path.abspath(block_template)),data_file('blocks')]))

    # index all of the source files
    print('Starting 🔥')
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

    # Second pass to process all of the output templates and resolve the {{SRC_PATH}} variable
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
# 🚗
# 🚗