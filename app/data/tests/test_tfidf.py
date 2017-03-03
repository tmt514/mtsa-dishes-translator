from app.tests.test_app import AAFoodTestCase
from app.data.pokemon_crawler import tfidf

class TestTFIDF(AAFoodTestCase):
    
    def no_test_import_tfidf(self):
        tfidf()
        
