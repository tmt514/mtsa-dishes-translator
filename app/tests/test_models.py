from app.tests.test_app import AAFoodTestCase
from app.models import db, Term, Category, Termcategories, Photo
class ModelTestCase(AAFoodTestCase):

    def test_categories(self):


        for x in Category.query.all():
            print(x.name, x.parent)

        term = Term.query.filter_by(english="pikachu", chinese="皮卡丘").first()
        print(term)

        print(list(map(lambda x: x.name, term.categories.all())))
        print(list(map(lambda x: x.content, term.descriptions.all())))
        print(list(map(lambda x: x.as_dict(), term.photos.all())))

