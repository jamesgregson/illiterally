import os

# 🚀 Utility functions
def root_dir(): 
    return os.path.dirname( __file__ ) 

def data_file( *args ): 
    return os.path.join( root_dir(), 'data', *args )

def read_file( prefix, file ):
    fname = os.path.join( prefix, file )
    return open( fname ).read()
# 🚗