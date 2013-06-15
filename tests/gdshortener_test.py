import gdshortener
import unittest


class GDShortenerTest(unittest.TestCase):


    def setUp(self):
        self._tested = gdshortener.GDBaseShortener(timeout=30)
        self._tested_is = gdshortener.ISGDShortener(timeout=30)
        self._tested_v = gdshortener.VGDShortener()


    def tearDown(self):
        pass


    def testShorten(self):
        shortened_url, stat_url = self._tested.shorten(
                                             url = "http://maps.google.co.uk/maps?f=q&source=s_q&hl=en&geocode=&q=louth&sll=53.800651,-4.064941&sspn=33.219383,38.803711&ie=UTF8&hq=&hnear=Louth,+United+Kingdom&ll=53.370272,-0.004034&spn=0.064883,0.075788&z=14")
        self.assertIsNotNone(shortened_url)
        self.assertIsNone(stat_url)
        print "Url obtained: [{0}]".format(shortened_url)

    def testShortenWithCustomUrl(self):
        self.assertRaises(gdshortener.GDShortURLError, self._tested.shorten, "http://maps.google.co.uk/maps?f=q&source=s_q&hl=en&geocode=&q=louth&sll=53.800651,-4.064941&sspn=33.219383,38.803711&ie=UTF8&hq=&hnear=Louth,+United+Kingdom&ll=53.370272,-0.004034&spn=0.064883,0.075788&z=14", 'GooglE')

    def testShortenWithLog(self):
        shortened_url, stat_url = self._tested.shorten(
                                             url = "http://maps.google.co.uk/maps?f=q&source=s_q&hl=en&geocode=&q=louth&sll=53.800651,-4.064941&sspn=33.219383,38.803711&ie=UTF8&hq=&hnear=Louth,+United+Kingdom&ll=53.370272,-0.004034&spn=0.064883,0.075788&z=14",
                                             log_stat= True)
        self.assertIsNotNone(shortened_url)
        self.assertIsNotNone(stat_url)
        print "Url obtained: [{0}] - Stat url obtained: [{1}]".format(shortened_url, stat_url)
        
    def testLookupShortenUrl(self):
        shortened_url, stat_url = self._tested.shorten(
                                             url = "http://maps.google.co.uk/maps?f=q&source=s_q&hl=en&geocode=&q=louth&sll=53.800651,-4.064941&sspn=33.219383,38.803711&ie=UTF8&hq=&hnear=Louth,+United+Kingdom&ll=53.370272,-0.004034&spn=0.064883,0.075788&z=14")
        self.assertIsNotNone(shortened_url)
        self.assertIsNone(stat_url)
        original_url = self._tested.lookup(shortened_url)
        self.assertIsNotNone(original_url)
        print "Url obtained: [{0}] - Lookup url: [{1}]".format(shortened_url, original_url)
        
    def testVShorten(self):
        shortened_url, stat_url = self._tested_v.shorten(
                                             url = "http://maps.google.co.uk/maps?f=q&source=s_q&hl=en&geocode=&q=louth&sll=53.800651,-4.064941&sspn=33.219383,38.803711&ie=UTF8&hq=&hnear=Louth,+United+Kingdom&ll=53.370272,-0.004034&spn=0.064883,0.075788&z=14")
        self.assertIsNotNone(shortened_url)
        self.assertIsNone(stat_url)
        print "Url obtained: [{0}]".format(shortened_url)

    def testVShortenWithCustomUrl(self):
        self.assertRaises(gdshortener.GDShortURLError, self._tested.shorten, "http://maps.google.co.uk/maps?f=q&source=s_q&hl=en&geocode=&q=louth&sll=53.800651,-4.064941&sspn=33.219383,38.803711&ie=UTF8&hq=&hnear=Louth,+United+Kingdom&ll=53.370272,-0.004034&spn=0.064883,0.075788&z=14", 'GooglE')

    def testVShortenWithLog(self):
        shortened_url, stat_url = self._tested_v.shorten(
                                             url = "http://maps.google.co.uk/maps?f=q&source=s_q&hl=en&geocode=&q=louth&sll=53.800651,-4.064941&sspn=33.219383,38.803711&ie=UTF8&hq=&hnear=Louth,+United+Kingdom&ll=53.370272,-0.004034&spn=0.064883,0.075788&z=14",
                                             log_stat= True)
        self.assertIsNotNone(shortened_url)
        self.assertIsNotNone(stat_url)
        print "Url obtained: [{0}] - Stat url obtained: [{1}]".format(shortened_url, stat_url)
        
    def testVLookupShortenUrl(self):
        shortened_url, stat_url = self._tested_v.shorten(
                                             url = "http://maps.google.co.uk/maps?f=q&source=s_q&hl=en&geocode=&q=louth&sll=53.800651,-4.064941&sspn=33.219383,38.803711&ie=UTF8&hq=&hnear=Louth,+United+Kingdom&ll=53.370272,-0.004034&spn=0.064883,0.075788&z=14")
        self.assertIsNotNone(shortened_url)
        self.assertIsNone(stat_url)
        original_url = self._tested_v.lookup(shortened_url)
        self.assertIsNotNone(original_url)
        print "Url obtained: [{0}] - Lookup url: [{1}]".format(shortened_url, original_url)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()