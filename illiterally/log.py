import io

class Log:
    def __init__( self, log_file: str=None ):
        self.file = open( log_file, 'w' ) if log_file else None
        self.scope = 0
        self.errors = 0
        self.warnings = 0

    def indent( self ):
        return Indent( self )

    def error( self, *args, **kwargs ):
        self.errors += 1
        self.info( '[ERROR]: ', *args, **kwargs )

    def warning( self, *args, **kwargs ):
        self.warnings += 1
        self.info( '[WARNING]: ', *args, **kwargs )

    def info( self, *args, **kwargs ):
        with io.StringIO() as out:
            print( ' '*self.scope, *args, file=out, end=None )
            contents = out.getvalue()
        print( contents.rstrip() )
        if self.file is not None:
            self.file.write( contents )

class Indent(object):
    def __init__( self, log: Log ):
        self.log = log

    def __enter__( self ):
        self.log.scope += 1

    def __exit__( self, type, value, traceback ):
        self.log.scope -= 1