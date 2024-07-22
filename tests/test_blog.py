from tkinter import ttk

from tm4k.blog import Blog
from tm4k.fs.blog_file import *
import unittest

import tm4k.parse as parse

from tm4k.status_label import *


class TestCalculator(unittest.TestCase):
    def test_new(self):
        os.chdir("..")
        blog_id = "marcykatya"
        setStatusLabel(ttk.Label())
        posts_list = openBlogFile(blog_id)
        blog = Blog(posts_list)
        self.assertEqual(blog.blog_id,blog_id)


if __name__ == '__main__':
    unittest.main()
