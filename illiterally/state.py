from typing import *
import os
import jinja2
import urllib.parse

from .log import Log, Indent
from .utils import data_file, read_file
from .block import Block, BlockReader

class State:
    def __init__( self, source_files: list[str], template_files: list[str], block_template: str, output_dir: str='./output', source_prefix: Optional[str]=None, template_prefix: Optional[str]=None, left:str=None, right:str=None, source_url: Optional[str]=None, output_url: Optional[str]=None, suppress:bool=False, log_file:str=None ):
        # log file
        self.log = Log( log_file )
        self.log.info('🔥 Starting...')

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

        # output url prefix
        if (source_url and not output_url) or (output_url and not source_url):
            self.log.error('Must specify both or neither of "source_url" and "output_url"')

        self._source_url = source_url
        self._output_url = output_url

        # output delimiter suppression
        self.suppress = suppress

    def source_url( self, filename: str, target: str ):
        '''Generate a link to filename from target, where filename is in the source-tree and target is in the output-tree'''
        if self._source_url != '':
            # use absolute URLs if the source url has been provided, e.g. for deployment on a server
            return urllib.parse.urljoin( self._source_url, os.path.relpath( filename, self.source_prefix ) )
        # otherwise use relative paths, e.g. for in-source applications in a filesystem
        return os.path.relpath( filename, os.path.dirname(target) )

    def output_url( self, filename: str, target: str ):
        '''Generate a link to a filename from target, where filename and target are both in the output tree'''
        if self._output_url != '':
            # use absolute URLs if the output url has been provided, e.g. for deployment on a server
            return urllib.parse.urljoin( self._output_url, os.path.relpath( filename, self.output_dir ) )
        # otherwise use relative paths, e.g. for in-source applications in a filesystem
        return os.path.relpath( filename, os.path.dirname(target) )

    def ref( self, block: Block, target:str ):
        if block.rendered_into == target:
            return target
        return os.path.relpath( block.rendered_into, os.path.dirname(target) ) if self.rendered_into else 'INVALID'

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
                    file_blocks = BlockReader.index_blocks( source_file, duplicates=induplicates, left=self.left, right=self.right, suppress=self.suppress )
                    if file_blocks is None:
                        self.log.info(f'No blocks found in {source_file}, skipping.')
                        continue
                    self.log.info(f'Processing file: "{source_file}"...')
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

    def default_callbacks( self, blocks: Dict[str,Block], into: str ):
        '''Callbacks/state available for all templates'''
        return dict(
            __file__ = into,                
            source_url = self.source_url,
            output_url = self.output_url,
            block = lambda slug: self.block_from_slug(blocks,slug),
            reference = lambda block, target: self.ref( block, target ),
            suppress = self.suppress,
        )

    def activate_callbacks( self, blocks: Dict[str,Block], into: str, template: str ):
        '''Callbacks used in first pass to activate blocks that have been referenced'''
        return dict( 
            **self.default_callbacks( blocks, into ),
            render_block = lambda slug: self.activate_block_by_slug( blocks, slug, into ),
            include_file = lambda x: x
        )
    
    def render_callbacks( self, blocks: Dict[str,Block], into: str, template: str  ):
        '''Callbacks used in second pass to actually render the active blocks'''
        return dict( 
            **self.default_callbacks( blocks, into ),
            render_block = lambda slug: self.render_block_by_slug( blocks, slug, into ), 
            include_file = lambda x: read_file( os.path.dirname(template), x )
        )

    def render_block_by_slug( self, blocks: Dict[str,Block], slug: str, into: str ):
        with self.log.indent():
            if slug in blocks:
                if blocks[slug].rendered_into != into:
                    self.log.error(f'Block {slug} already rendered by "{blocks[slug].rendered_into}".')
                    return None
                self.log.info(f'Rendered block {slug} for template "{into}".')
                return self.blk_template.render( **self.default_callbacks(blocks,into), slug=slug )
            else:
                self.log.warning(f'Referenced non-existent slug "{slug}".')
                return None

    def activate_blocks_from_templates( self, blocks: Dict[str,Block] ):
        with self.log.indent():
            self.log.info('Activating blocks from templates...')
            with self.log.indent():
                for template_file,output_file in zip(self.template_files,self.output_files):
                    self.log.info(f'Template file: {template_file}...')
                    template = self.env.from_string( open(template_file).read() )
                    template.render( **self.activate_callbacks( blocks, output_file, template_file ) )

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