from reviewboard.site.urlresolvers import local_site_reverse

    def test_with_filenames_option(self):
        """Testing ReviewsDiffViewerView with ?filenames=..."""
        review_request = self.create_review_request(create_repository=True,
                                                    publish=True)
        diffset = self.create_diffset(review_request)
        filediff1 = self.create_filediff(diffset,
                                         source_file='src/main/test.c',
                                         dest_file='src/main/test.cpp')
        filediff2 = self.create_filediff(diffset,
                                         source_file='docs/README.txt',
                                         dest_file='docs/README2.txt')
        filediff3 = self.create_filediff(diffset,
                                         source_file='test.txt',
                                         dest_file='test.rst')
        filediff4 = self.create_filediff(diffset,
                                         source_file='/lib/lib.h',
                                         dest_file='/lib/lib.h')
        self.create_filediff(diffset,
                             source_file='unmatched',
                             dest_file='unmatched')

        response = self.client.get(
            local_site_reverse(
                'view-diff-revision',
                kwargs={
                    'review_request_id': review_request.display_id,
                    'revision': diffset.revision,
                }),
            {
                'filenames': '*/test.cpp,*.txt,/lib/*',
            })
        self.assertEqual(response.status_code, 200)

        files = response.context['files']
        self.assertEqual({file_info['filediff'] for file_info in files},
                         {filediff1, filediff2, filediff3, filediff4})

    def test_with_filenames_option_normalized(self):
        """Testing ReviewsDiffViewerView with ?filenames=... values normalized
        """
        review_request = self.create_review_request(create_repository=True,
                                                    publish=True)
        diffset = self.create_diffset(review_request)
        filediff1 = self.create_filediff(diffset,
                                         source_file='src/main/test.c',
                                         dest_file='src/main/test.cpp')
        filediff2 = self.create_filediff(diffset,
                                         source_file='docs/README.txt',
                                         dest_file='docs/README2.txt')
        filediff3 = self.create_filediff(diffset,
                                         source_file='test.txt',
                                         dest_file='test.rst')
        filediff4 = self.create_filediff(diffset,
                                         source_file='/lib/lib.h',
                                         dest_file='/lib/lib.h')
        self.create_filediff(diffset,
                             source_file='unmatched',
                             dest_file='unmatched')

        response = self.client.get(
            local_site_reverse(
                'view-diff-revision',
                kwargs={
                    'review_request_id': review_request.display_id,
                    'revision': diffset.revision,
                }),
            {
                'filenames': ' ,  , */test.cpp,,,*.txt,/lib/*  ',
            })
        self.assertEqual(response.status_code, 200)

        files = response.context['files']
        self.assertEqual({file_info['filediff'] for file_info in files},
                         {filediff1, filediff2, filediff3, filediff4})