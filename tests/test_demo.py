import os

import illiterally

from utils import run_in_temp_directory

@run_in_temp_directory()
def test_demo( test_dir: str=None ):
    illiterally.illiterally_demo()
    illiterally.illiterally_cli( open('run.sh').read().split() )
    assert os.path.exists('output/example.md')

if __name__ == '__main__':
    test_demo()