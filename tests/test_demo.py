import os

import illiterally

from utils import run_in_temp_directory

@run_in_temp_directory()
def test_demo( test_dir: str=None ):
    illiterally.cli.illiterally_demo()
    illiterally.cli.illiterally_cli( open('run.sh').read().split() )
    assert os.path.exists('output/example.md')

if __name__ == '__main__':
    test_demo()