import os
import shutil 

def exclude_from_tests( fn ):
    '''Decorated functions should not be treated as test cases by pytest'''
    fn.__test__ = False
    return fn

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

@exclude_from_tests
def test_data_dir():
    return os.path.join( os.path.dirname(__file__), 'test_data' )