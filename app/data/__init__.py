from .parsepokemon import add_pokemons
from .parsejokes import add_jokes
from .parsecategories import add_categories

from app.models import db, Category, Term, Photo, Joke
import os
import pickle

if os.path.exists('app/data/pokemon_names_mapping') == False:
    print("\033[1;34mDownloading Pokemon Data\033[m")
    os.system("wget \"https://drive.google.com/uc?id=0BzTEEqZlZigxU2RQdHp4MmFYX00&export=download\" -O app/data/pokemon_names_mapping")
    os.system("wget \"https://drive.google.com/uc?id=0BzTEEqZlZigxVGZhQ0pEeFNkN1E&export=download\" -O app/data/pokemon_reverse_index")
    os.system("wget \"https://drive.google.com/uc?id=0BzTEEqZlZigxbE90eHFmUDY0VEE&export=download\" -O app/data/pokemon_doc_freq")

POKEMON_REVERSE_INDEX = pickle.load(open('app/data/pokemon_reverse_index', 'rb'))
POKEMON_NAMES_MAPPING = pickle.load(open('app/data/pokemon_names_mapping', 'rb'))

def add_data():
    if Category.query.count() == 0:
        print("\033[1;34mAdding Categories\033[m")
        add_categories()
        print(Category.query.count())
    if Term.query.filter_by(english='pikachu').first() == None:
        print("\033[1;34mAdding Pokemons\033[m")
        add_pokemons()
        print(Term.query.count())
    if Joke.query.count() == 0:
        print("\033[1;34mAdding Jokes\033[m")
        add_jokes()
        print(Joke.query.count())
