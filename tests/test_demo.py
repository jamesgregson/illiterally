import os
import tempfile

import illiterally
import illiterally.cli

def run_in_temp_directory():
    def decorator( fn: callable ):
        def wrapper( *args, **kwargs ):
            cwd = os.getcwd()
            with tempfile.TemporaryDirectory() as test_dir:
                print(f'running test in {test_dir}')
                os.chdir( test_dir )
                fn( *args, test_dir=test_dir, **kwargs )
            os.chdir(cwd)
        return wrapper
    return decorator    

@run_in_temp_directory()
def test_demo( test_dir: str=None ):
    illiterally.cli.illiterally_demo()
    illiterally.cli.illiterally_cli( open('run.sh').read().split() )
    assert os.path.exists('output/example.md')

if __name__ == '__main__':
    test_demo()