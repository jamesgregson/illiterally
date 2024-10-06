import os
import shutil 

def run_in_temp_directory():
    def decorator( fn: callable ):
        def wrapper( *args, **kwargs ):
            cwd = os.getcwd()
            test_dir = os.path.join( os.path.dirname(__file__), 'runs', fn.__name__ )
            shutil.rmtree( test_dir, ignore_errors=True )
            os.makedirs( test_dir )
            print(f'running test in {test_dir}')
            os.chdir( test_dir )
            fn( *args, test_dir=test_dir, **kwargs )
            os.chdir(cwd)
        return wrapper
    return decorator

def test_data_dir():
    return os.path.join( os.path.dirname(__file__), 'test_data' )