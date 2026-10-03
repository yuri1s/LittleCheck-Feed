import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock

from export_github_site import export_site


class ExportTests(unittest.TestCase):
    def test_split_rewrite_cache_and_no_input_mutation(self):
        url = 'https://origin.test/media/0123456789abcdef.webp'
        entry = {'id': 'rss:demo:1', 'title': 't', 'summary': 's', 'content': f'![image]({url})',
                 'source': 'Demo', 'platform': 'other', 'published_at': '2026-10-03T00:00:00Z'}
        feed = {'schema_version': 1, 'generated_at': entry['published_at'], 'items': [entry]}
        download = Mock(return_value=b'RIFF0000WEBPtest')
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ['first', 'second']:
                output = root / name
                export_site(feed, output, root/'cache', 'https://user.github.io/repo', 'https://origin.test/media', download)
                self.assertTrue((output/'feeds/rss-demo.json').exists())
                published = json.loads((output/'feed.json').read_text())
                self.assertIn('https://user.github.io/repo/media/', published['items'][0]['content'])
            self.assertEqual(download.call_count, 1)
            self.assertEqual(feed['items'][0]['content'], f'![image]({url})')

    def test_image_failure_aborts_before_feed_publication(self):
        entry = {'id': 'gh:demo', 'title': 't', 'summary': 's', 'content': '![i](https://origin.test/media/0123456789abcdef.webp)',
                 'source': 'GitHub', 'platform': 'github', 'published_at': '2026-10-03T00:00:00Z'}
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            with self.assertRaises(ValueError):
                export_site({'schema_version': 1, 'generated_at': entry['published_at'], 'items': [entry]},
                            root/'site', root/'cache', 'https://user.github.io/repo', 'https://origin.test/media',
                            lambda *_: b'<html>Error</html>')
            self.assertFalse((root/'site/feed.json').exists())

    def test_platform_subscriptions_follow_feed_values_dynamically(self):
        def entry(identity, platform):
            return {'id': identity, 'title': 't', 'summary': 's', 'content': '',
                    'source': 's', 'platform': platform, 'published_at': '2026-10-03T00:00:00Z'}
        feed = {'schema_version': 2, 'generated_at': '2026-10-03T00:00:00Z', 'items': [
            entry('gh:1', 'github'), entry('ma:1', 'Mastodon'), entry('bo:1', '博客'),
            entry('no:1', None), entry('blank:1', '  ')]}
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subscriptions = export_site(feed, root/'site', root/'cache',
                                        'https://user.github.io/repo', 'https://origin.test/media')
            self.assertEqual({s['name'] for s in subscriptions}, {'全部', 'github', 'Mastodon', '博客', 'other'})
            self.assertTrue((root/'site/feeds/github.json').exists())
            self.assertTrue((root/'site/feeds/Mastodon.json').exists())
            self.assertTrue((root/'site/feeds/%E5%8D%9A%E5%AE%A2.json').exists())
            self.assertTrue((root/'site/feeds/other.json').exists())


if __name__ == '__main__':
    unittest.main()
