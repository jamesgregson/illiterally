import os
import sys
import glob
import shutil
import argparse

from .utils import data_file, root_dir
from .illiterally import illiterally

def illiterally_cli( argv=sys.argv ):
    parser = argparse.ArgumentParser('illiterally')
    parser.add_argument('-s',           '--source', type=str, nargs='+', required=True,      help='Source file')
    parser.add_argument('-b',            '--block', type=str,            required=True,      help='Block template')
    parser.add_argument('-o',         '--template', type=str, nargs='+', required=True,      help='Output template')
    parser.add_argument('-sp',   '--source-prefix', type=str,            default='.',        help='Prefix removed from source filenames in output')
    parser.add_argument('-op', '--template-prefix', type=str,            default='.',        help='Prefix removed from output filenames')
    parser.add_argument('-od',      '--output-dir', type=str,            default='./output', help='Save output files relative to this directory' )
    parser.add_argument( '-x',        '--suppress', action='store_true',                     help='Provide empty strings to templates as delimiters')
    parser.add_argument('-l',             '--left', type=str,            default=None,       help='Optional: Left bracket string')
    parser.add_argument('-r',            '--right', type=str,            default=None,       help='Optional: Right bracket string')
    
    try:
        args = parser.parse_args( argv[1:] )   
        assert (args.left and args.right) or (not args.left and not args.right) 
    except:
        sys.exit()

    kwargs = dict(
        source_files     = args.source,
        template_files   = args.template,
        block_template   = args.block,
        suppress         = args.suppress,
        source_prefix    = args.source_prefix,
        template_prefix  = args.template_prefix,
        output_dir       = args.output_dir,
    )
    if args.left and args.right:
        kwargs['left']  = args.left
        kwargs['right'] = args.right

    return illiterally( **kwargs )

def illiterally_demo():
    shutil.copyfile( data_file('examples/docs/example.cpp'), './example.cpp' )
    shutil.copyfile( data_file('examples/docs/example.md'),  './example.md' )
    with open('run.sh','w') as sh:
        sh.write('illiterally --source example.cpp --block block.md --template example.md')
    print('Demo files created, now run: chmod +x run.sh && ./run.sh')

def illiterally_dogfood():
    # must be first since brackets are not auto-detected with text delimiters
    illiterally( 
        source_files=[data_file('examples/docs/nomoji.cpp')],
        block_template='block.md',
        template_files=[data_file('examples/docs/nomoji.md')],
        left = '<<<:', right = ':>>>',
        template_prefix=data_file('examples'),
        output_dir=data_file('../..'),
    )

    illiterally(
        source_files=sorted(glob.glob(os.path.join(root_dir(),'*.py'))),
        block_template='block.md',
        template_files=[ data_file('examples/README.md'), data_file('examples/docs/implementation.md') ],
        template_prefix=data_file('examples'),
        output_dir=data_file('../..')
    )

    illiterally( 
        source_files=[ data_file('examples/docs/example.cpp') ],
        block_template='block.md',
        template_files=[ data_file('examples/docs/example.md') ],
        template_prefix=data_file('examples'),
        output_dir=data_file('../..'),
    )

    illiterally( 
        source_files=[ data_file('examples/docs/handmoji.cpp') ],
        block_template='block.md',
        template_files=[ data_file('examples/docs/handmoji.md') ],
        template_prefix=data_file('examples'),
        output_dir=data_file('../..'),
    )

    illiterally(
        source_files=[ data_file('examples/docs/example.cpp') ],
        block_template='block.tex',
        template_files=[ data_file('examples/docs/example.tex') ],
        template_prefix=data_file('examples'),
        output_dir=data_file('../..'),
        suppress=True
    )

    illiterally(
        source_files=[ data_file('examples/docs/example.cpp') ],
        block_template='block.html',
        template_files=[ data_file('examples/docs/example.html') ],
        template_prefix=data_file('examples'),
        output_dir=data_file('../..'),
    )
