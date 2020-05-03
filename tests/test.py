import unittest


class TestSum(unittest.TestCase):

    def test_import_and_iamge_compare(self):
        try:
            from os import sys, path
            #sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
            sys.path.append('./')
            import camerabot.file_utils as file_utils
            import camerabot.images_utils as images_utils
            
            file1 = path.join(path.dirname(path.abspath(__file__)), '1.jpg')
            file2 = path.join(path.dirname(path.abspath(__file__)), '2.jpg')
            images_utils.compare_two_images_3(file1, file2)
        except  Exception as e:
            self.fail("Imports raised Exception unexpectedly! {}".format(str(e)))


        # def test_sum_tuple(self):
        #     self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()






