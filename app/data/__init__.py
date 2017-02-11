from .parsedishes import add_dishes
from .parsevegetables import add_vegetables


def prepare_data(dryrun=True):
    add_dishes(dryrun)
    add_vegetables(dryrun)

