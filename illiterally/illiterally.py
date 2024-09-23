# 🚀 Illiterally Implementation
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
    rendered:      str = None
    rendered_into: str = None

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

    def source_path( self, targ: str ):
        return os.path.relpath( self.filename, os.path.dirname(targ) )

    def ref(self, targ: str ):
        if self.rendered_into == targ:
            return ''
        return os.path.relpath( self.rendered_into, os.path.dirname(targ) ) if self.rendered_into else 'INVALID'
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

    # load the block template
    print(f'  Loading block template: {block_template}')
    blk_template = env.from_string( open(block_template).read() )
    
    # generate index of all blocks in the source files
    blocks = {}
    duplicates, invalid = set(), set()
    print('  Building index:')
    for source_file in source_files:
        print(f'    Processing file: {os.path.abspath(source_file)}')
        file_blocks = BlockReader.index_blocks( source_file, left=left, right=right, suppress=suppress )
        for key,blk in file_blocks.items():
            if key in blocks: 
                print(f'      WARNING: Block "{key}" already exists, skipping.')
                duplicates.add(key)
            else:
                print(f'      Found block at line {blk.line}: {blk.name}, key={key}') 
                blocks[key] = blk

    def is_valid( slug: str ):
        if slug not in blocks:
            invalid.add(slug)
            return False
        return True

    def block_cb( slug: str ):
        return blocks[slug] if is_valid(slug) else None
    
    def render_cb1( out_file: str, slug: str ):
        print(f'      Block: {slug}')
        return blocks[slug].activate(out_file) if is_valid(slug) else None

    # first pass over the output templates to flag which blocks get rendered by the output templates
    print('  Building active block list...')
    for template_file in output_files:
        print(f'    Template file: {template_file}...')
        out_file = os.path.abspath( os.path.join( output_dir, os.path.relpath(template_file,output_prefix) ) )
        template = env.from_string( open(template_file).read() )
        template.render( __file__ = out_file, block=block_cb, render_block=lambda slug: render_cb1(out_file,slug), include_file=lambda x: x )

    # Second pass to process all of the output templates and resolve the {{SRC_PATH}} variable
    print(f'  Rendering output files...')
    for template_file in output_files:
        print(f'    Rendering template: {template_file}...')
        out_file = os.path.abspath( os.path.join( output_dir, os.path.relpath(template_file,output_prefix) ) )
        os.makedirs( os.path.dirname( out_file ), exist_ok=True )
        print(f'    Rendering file: {os.path.abspath(out_file)}')

        def render_cb( slug ):
            print(f'      Block: {slug}')
            return blk_template.render( __file__ = out_file, slug=slug, block=block_cb, blocks=blocks, suppress=suppress ) if is_valid(slug) else None

        template = env.from_string( open(template_file).read() )
        with open( out_file, 'w' ) as outf:
            outf.write( template.render( __file__ = out_file, block=block_cb, render_block=render_cb, include_file=lambda x: read_file(source_prefix,x) ))

    if duplicates:
        print(f'Duplicate blocks found: {" ".join([blk for blk in duplicates])}')
    if invalid:
        print(f'Invalid blocks referenced: {" ".join([blk for blk in invalid])}')

    if len(duplicates) == 0 and len(invalid) == 0:
        print('🔥 finished successfully!')
        return 0
    else:
        print('🔥 completed with errors!')
        return 1
# 🚗
# 🚗