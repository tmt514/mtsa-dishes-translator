from .parsepokemon import add_pokemons
from .parsejokes import add_jokes

def add_data(dryrun=True):
    add_pokemons(dryrun)
    add_jokes(dryrun)
