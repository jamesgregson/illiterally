import os
import glob
import illiterally as ill

from utils import test_data_dir

def test_state_paths():
    S = ill.State( 
        source_files = glob.glob( os.path.join( test_data_dir(), 'source_files/source*.txt' ) ),
        template_files = glob.glob( os.path.join( test_data_dir(), 'template_files/output*.txt' ) ),
        block_template='block.md',
        output_dir='blah/output_test'
    )

    assert S.source_prefix == os.path.join( test_data_dir(), 'source_files' )
    assert S.template_prefix == os.path.join( test_data_dir(), 'template_files' )

    for f in S.source_files:
        assert os.path.exists( f )

    for f in S.template_files:
        assert os.path.exists( f )

    for t,o in zip( S.template_files, S.output_files ):
        assert os.path.abspath( os.path.join( S.output_dir, os.path.relpath( t, S.template_prefix ) ) ) == o

if __name__ == '__main__':
    test_state_paths()

