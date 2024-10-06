import sys
from illiterally.cli import illiterally_cli, illiterally_demo, illiterally_dogfood

def illiterally_cli_entry_point( argv=sys.argv ):
    return illiterally_cli( argv )

def illiterally_demo_entry_point():
    return illiterally_demo()

def illiterally_dogfood_entry_point():
    return illiterally_dogfood()

if __name__ == '__main__':
    illiterally_dogfood()