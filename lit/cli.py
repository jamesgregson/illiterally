import os
import sys
import stat
import shutil
import argparse

from lit import lit, data_file, root_dir

def lit_cli( argv=sys.argv ):
    parser = argparse.ArgumentParser('lit')
    parser.add_argument('-s',         '--source', type=str, required=True,      help='Source file')
    parser.add_argument('-b',          '--block', type=str, required=True,      help='Block template')
    parser.add_argument('-o',         '--output', type=str, required=True,      help='Output template')
    parser.add_argument('-sp', '--source-prefix', type=str, default='.',        help='Prefix removed from source filenames in output')
    parser.add_argument('-op', '--output-prefix', type=str, default='.',        help='Prefix removed from output filenames')
    parser.add_argument('-od',    '--output_dir', type=str, default='./output', help='Save output files relative to this directory' )
    parser.add_argument( '-x',      '--suppress',      action='store_true',     help='Provide empty strings to templates as delimiters')
    parser.add_argument('-l',           '--left', type=str, default=None,       help='Optional: Left bracket string')
    parser.add_argument('-r',          '--right', type=str, default=None,       help='Optional: Right bracket string')
    
    try:
        args = parser.parse_args( argv[1:] )   
        assert (args.left and args.right) or (not args.left and not args.right) 
    except:
        sys.exit()

    kwargs = dict(
        source_files   = [args.source],
        block_template = args.block,
        output_files   = [args.output],
        suppress       = args.suppress,
        source_prefix  = args.source_prefix,
        output_prefix  = args.output_prefix,
        output_dir     = args.output_dir,
    )
    if args.left and args.right:
        kwargs['left']  = args.left
        kwargs['right'] = args.right

    lit( **kwargs )

def lit_demo():
    shutil.copyfile( data_file('examples/docs/example.cpp'), './example.cpp' )
    shutil.copyfile( data_file('examples/docs/example.md'),  './example.md' )
    with open('run.sh','w') as sh:
        sh.write('lit --source example.cpp --block block.md --output example.md')
    print('Demo files created, now run: chmod +x run.sh && ./run.sh')

def lit_dogfood():
    # must be first since brackets are not auto-detected with text delimiters
    lit( 
        source_files=[data_file('examples/docs/nomoji.cpp')],
        block_template='block.md',
        output_files=[data_file('examples/docs/nomoji.md')],
        left = '<<<:', right = ':>>>',
        output_prefix=data_file('examples'),
        output_dir=data_file('../..'),
    )

    lit(
        source_files=[data_file('../lit.py')],
        block_template='block.md',
        output_files=[ data_file('examples/README.md') ],
        output_prefix=data_file('examples'),
        output_dir=data_file('../..')
    )

    lit( 
        source_files=[ data_file('examples/docs/example.cpp') ],
        block_template='block.md',
        output_files=[ data_file('examples/docs/example.md') ],
        output_prefix=data_file('examples'),
        output_dir=data_file('../..'),
    )

    lit( 
        source_files=[ data_file('examples/docs/handmoji.cpp') ],
        block_template='block.md',
        output_files=[ data_file('examples/docs/handmoji.md') ],
        output_prefix=data_file('examples'),
        output_dir=data_file('../..'),
    )


if __name__ == '__main__':
    lit_dogfood()