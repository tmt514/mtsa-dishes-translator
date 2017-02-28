from .parsepokemon import add_pokemons
from .parsejokes import add_jokes
from .parsecategories import add_categories

def add_data(dryrun=True):
    add_categories(dryrun)
    add_pokemons(dryrun)
    add_jokes(dryrun)
