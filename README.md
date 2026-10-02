# Little Check Feed

Public feed mirror for Little Check. The VPS collects the content; GitHub Actions reads the public JSON and cached WebP images, then publishes a GitHub Pages artifact every hour. Generated content is not committed to Git history.

Feed: https://yuri1s.github.io/LittleCheck-Feed/feed.json
Subscriptions: https://yuri1s.github.io/LittleCheck-Feed/subscriptions.json

The feed is a snapshot, not a reverse proxy. Failed builds retain the last successful deployment. Publication keeps source timestamps. Cached images are retained for up to seven days subject to GitHub Actions cache availability. Images not cached by the source remain external URLs.

Only public feed content is mirrored. No personal notes, login sessions, API credentials, or VPS logs are included. Source filters are not a guarantee of content review; all published content remains subject to GitHub policies.

Set Pages source to GitHub Actions and set repository variable PAGES_BASE_URL to https://yuri1s.github.io/LittleCheck-Feed. FEED_SOURCE and FEED_MEDIA_BASE default to the current public VPS feed and media URLs. Scheduled Actions may be delayed and may pause after prolonged repository inactivity.

Tests: python -B -m unittest discover -s server -v