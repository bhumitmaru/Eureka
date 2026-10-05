import unittest
from services.data_cleaner import clean_paper, normalize_title
from services.deduplicator import deduplicate
from services.ranking import rank

class CoreTests(unittest.TestCase):
 def test_cleaning(self):
  p=clean_paper({'title':'  <b>Deep Learning</b> ','authors':' A  B ','citation_count':'3'})
  self.assertEqual(p['title'],'Deep Learning'); self.assertEqual(p['citation_count'],3)
 def test_title_normalization(self): self.assertEqual(normalize_title('DEEP Learning! '),normalize_title('deep learning'))
 def test_deduplication_map(self):
  papers=[clean_paper({'title':'A paper','doi':'10/x','citation_count':1}),clean_paper({'title':'A PAPER ','doi':'10/x','citation_count':2})]
  kept, removed=deduplicate(papers); self.assertEqual((len(kept),removed,kept[0]['citation_count']),(1,1,2))
 def test_ranking(self): self.assertGreater(rank([clean_paper({'title':'Machine learning in health'})],'machine learning')[0]['relevance'],0)
if __name__=='__main__': unittest.main()
