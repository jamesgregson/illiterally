# 🚀 Illiterally Implementation
from typing import *
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

    # def activate(self,into:str):
    #     assert self.rendered_into in [None,into]
    #     self.rendered_into = os.path.abspath(into)
    #     return ''

    # def render(self,into: str):
    #     assert self.rendered_into in [None,into]
    #     return self.rendered.replace( '{{SRC_PATH}}',os.path.relpath(self.filename,os.path.dirname(self.rendered_into)))

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
    def index_blocks( filename: str, *args, duplicates: Set[str]=None, left: str=None, right:str=None, **kwargs ):
        if left is None or right is None:
            left,right = BlockReader.detect_left_right( filename )
            if None in [left,right]:
                raise RuntimeWarning(f'Error parsing: {filename}, autodetection of delimiters failed.')

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



# 🚀 Entry-point
class Log:
    def __init__( self, log_file: str=None ):
        self.file = open( log_file, 'w' ) if log_file else None
        self.scope = 0
        self.errors = 0
        self.warnings = 0

    def indent( self ):
        return Indent( self )

    def error( self, *args, **kwargs ):
        self.errors += 1
        self.info( '[ERROR]: ', *args, **kwargs )

    def warning( self, *args, **kwargs ):
        self.warnings += 1
        self.info( '[WARNING]: ', *args, **kwargs )

    def info( self, *args, **kwargs ):
        with io.StringIO() as out:
            print( ' '*self.scope, *args, file=out, end=None )
            contents = out.getvalue()
        print( contents.rstrip() )
        if self.file is not None:
            self.file.write( contents )

class Indent(object):
    def __init__( self, log: Log ):
        self.log = log

    def __enter__( self ):
        self.log.scope += 1

    def __exit__( self, type, value, traceback ):
        self.log.scope -= 1

class State:
    def __init__( self, source_files: list[str], template_files: list[str], block_template: str, output_dir: str='./output', source_prefix: Optional[str]=None, template_prefix: Optional[str]=None, left:str=None, right:str=None, suppress:bool=False, log_file:str=None ):
        # log file
        self.log = Log( log_file )
        self.log.info('Starting 🔥')

        # source files contain the source of blocks and source_prefix
        # defines the root directory with which relative paths are defined
        self.source_files = [os.path.abspath(f) for f in source_files]
        self.source_prefix = source_prefix or os.path.commonprefix([os.path.dirname(f) for f in self.source_files])
    
        # template files are the unprocessed 'output files' and the
        # template prefix defines the root directory with which 
        # relative paths are defined
        self.template_files = [os.path.abspath(f) for f in template_files]
        self.template_prefix = template_prefix or os.path.commonprefix([os.path.dirname(f) for f in self.template_files])

        # define the template search paths
        self.block_template_file = os.path.abspath(block_template) if os.path.exists(block_template) else os.path.join(data_file('blocks',block_template))
        self.template_search_paths = [ os.path.abspath(p) for p in [os.path.dirname(self.block_template_file),self.template_prefix,data_file('blocks')] ]

        # the output_dir is where output files will be written
        self.output_dir   = os.path.abspath( output_dir )
        self.output_files = [ os.path.abspath(os.path.join( self.output_dir, os.path.relpath(f,self.template_prefix))) for f in self.template_files ]

        # check that we're not going to clobber inputs
        with self.log.indent():
            input_files = set([*self.source_files,*self.template_files,self.block_template_file])
            for o in self.output_files:
                if o in input_files:
                    self.log.error('Output file "{o}" would overwrite source/template/block file.')

        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.template_search_paths))
        self.blk_template = self.env.from_string( open(self.block_template_file).read() )

        # the left and right delimiters, if auto-detection is not used
        self.left = left
        self.right = right 

        # output delimiter suppression
        self.suppress = suppress

    def parse_blocks( self, induplicates: Set[str]=None ):
        with self.log.indent():
            if induplicates is None:
                self.log.info('Building active slug index...')
            else:
                self.log.info('De-duplicating slugs & rebuilding index...')
            blocks = dict()
            duplicates = set()
            with self.log.indent():
                for source_file in sorted( self.source_files ):
                    self.log.info(f'Processing file: "{source_file}"...')
                    file_blocks = BlockReader.index_blocks( source_file, duplicates=induplicates, left=self.left, right=self.right, suppress=self.suppress )
                    for slug,block in file_blocks.items():
                        with self.log.indent():
                            if slug in blocks:
                                self.log.warning(f'Warning: Block with slug "{slug}" already exists.')
                                duplicates.add(slug)
                            else:
                                self.log.info(f'Found block at line {block.line}: {block.slug} = "{block.name}".')
                                blocks[slug] = block  
                if induplicates and len(duplicates) > 0:
                    self.log.error('Error: Duplicate slugs found during de-duplication. How???')

        return blocks,duplicates

    def block_from_slug( self, blocks: Dict[str,Block], slug: str ):
        with self.log.indent():
            if slug in blocks:
                return blocks[slug]
            self.log.warning(f'Warning: Referenced non-existent slug "{slug}".')
            return None
    
    def activate_block_by_slug( self, blocks: Dict[str,Block], slug: str, into: str ):
        with self.log.indent():
            if slug in blocks:
                self.log.info(f'Activated slug {slug} for template "{into}".')
                blk = blocks[slug]
                if blk.rendered_into is not None:
                    self.log.error(f'Block {slug} already activated by "{blk.rendered_into}".')
                    return None
                blocks[slug].rendered_into = into
            else:
                self.log.warning(f'Referenced non-existent slug "{slug}".')
            return None

    def render_block_by_slug( self, blocks: Dict[str,Block], slug: str, into: str ):
        with self.log.indent():
            if slug in blocks:
                if blocks[slug].rendered_into != into:
                    self.log.error(f'Block {slug} already rendered by "{blocks[slug].rendered_into}".')
                    return None
                self.log.info(f'Rendered block {slug} for template "{into}".')
                return self.blk_template.render( __file__ = into, slug=slug, block=lambda slug: self.block_from_slug( blocks, slug ), blocks=blocks, suppress=self.suppress )
            else:
                self.log.warning(f'Referenced non-existent slug "{slug}".')
                return None

    def activate_callbacks( self, blocks: Dict[str,Block], into: str, template: str ):
        return dict( __file__ = into, block = lambda slug: self.block_from_slug(blocks,slug), render_block = lambda slug: self.activate_block_by_slug( blocks, slug, into ), include_file = lambda x: x )
    
    def render_callbacks( self, blocks: Dict[str,Block], into: str, template: str  ):
        return dict( __file__ = into, block = lambda slug: self.block_from_slug(blocks,slug), render_block = lambda slug: self.render_block_by_slug( blocks, slug, into ), include_file = lambda x: read_file( os.path.dirname(template), x ) )

    def activate_blocks_from_templates( self, blocks: Dict[str,Block] ):
        with self.log.indent():
            self.log.info('Activating blocks from templates...')
            with self.log.indent():
                for template_file,output_file in zip(self.template_files,self.output_files):
                    self.log.info(f'Template file: {template_file}...')
                    template = self.env.from_string( open(template_file).read() )
                    template.render( **self.activate_callbacks( blocks, output_file ) )

    def render_blocks_from_templates( self, blocks: Dict[str,Block] ):
        with self.log.indent():
            self.log.info('Rendering blocks from templates...')
            with self.log.indent():
                for template_file,output_file in zip(self.template_files,self.output_files):
                    self.log.info(f'Template file: {template_file}...')
                    os.makedirs( os.path.dirname(output_file), exist_ok=True )
                    template = self.env.from_string( open(template_file).read() )
                    with open( output_file, 'w' ) as outf:
                        outf.write( template.render( **self.render_callbacks( blocks, output_file, template_file ) ) )


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




def illiterally2( source_files: list[str], template_files: list[str], block_template: list[str], left=None, right=None, source_prefix: str='.', template_prefix: str='.', output_dir: str='./output', suppress: bool=False ):
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
    for source_file in sorted(source_files):
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
    for template_file in template_files:
        print(f'    Template file: {template_file}...')
        out_file = os.path.abspath( os.path.join( output_dir, os.path.relpath(template_file,template_prefix) ) )
        template = env.from_string( open(template_file).read() )
        template.render( __file__ = out_file, block=block_cb, render_block=lambda slug: render_cb1(out_file,slug), include_file=lambda x: x )

    # Second pass to process all of the output templates and resolve the {{SRC_PATH}} variable
    print(f'  Rendering output files...')
    for template_file in template_files:
        print(f'    Rendering template: {template_file}...')
        out_file = os.path.abspath( os.path.join( output_dir, os.path.relpath(template_file,template_prefix) ) )
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