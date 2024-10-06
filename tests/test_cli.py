import os
import glob

import illiterally

from utils import run_in_temp_directory, test_data_dir

@run_in_temp_directory()
def test_txt( test_dir:str=None ):
    ret = illiterally.cli.illiterally_cli([ 'dummy',
        '--source',   *glob.glob( os.path.join( test_data_dir(), 'source_files/source*.txt') ),
        '--template', *glob.glob( os.path.join( test_data_dir(), 'template_files/output*.txt') ),
        '--template-prefix', test_data_dir(),
        '--block', 'block.txt',
        '--output-dir', test_dir
    ])
    assert ret == 0

if __name__ == '__main__':
    test_txt()