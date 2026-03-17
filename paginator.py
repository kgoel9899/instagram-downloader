import time
import random

class InstagramPaginator:
    def __init__(self, client, parser, username, max_count=float('inf')):
        self.client = client
        self.parser = parser
        self.username = username
        self.max_count = max_count
        self.downloaded_count = 0
        self.end_cursor = None
        self.has_next_page = True

    def __iter__(self):
        return self

    def __next__(self):
        if not self.has_next_page or self.downloaded_count >= self.max_count:
            raise StopIteration
        
        if self.end_cursor:
            delay = 1 + random.random() * 2
            print(f"Waiting {delay:.2f}s...")
            time.sleep(delay)

        print(f"Fetching batch... (End cursor: {self.end_cursor or 'null'})")
        batch_data = self.client.fetch_batch(self.username, self.end_cursor)
        
        media_items = self.parser.extract_media(batch_data)
        pagination_info = self.parser.get_pagination_info(batch_data)
        
        self.has_next_page = pagination_info['has_next_page']
        self.end_cursor = pagination_info['end_cursor']
        
        return media_items

    def update_count(self, count):
        self.downloaded_count += count


class CommentsPaginator:
    def __init__(self, client, parser, media_id, shortcode, max_comments=50):
        self.client = client
        self.parser = parser
        self.media_id = media_id
        self.shortcode = shortcode
        self.max_comments = max_comments
        self.fetched_count = 0
        self.end_cursor = None
        self.has_next_page = True

    def __iter__(self):
        return self

    def __next__(self):
        if not self.has_next_page or self.fetched_count >= self.max_comments:
            raise StopIteration
        
        if self.end_cursor:
            delay = 1 + random.random() * 2
            print(f"Waiting {delay:.2f}s for comments...")
            time.sleep(delay)

        print(f"Fetching comments batch... (End cursor: {self.end_cursor or 'null'})")
        batch_data = self.client.fetch_comments(self.media_id, self.shortcode, self.end_cursor)
        
        comments = self.parser.extract_comments(batch_data)
        pagination_info = self.parser.get_comments_pagination_info(batch_data)
        
        self.has_next_page = pagination_info['has_next_page']
        self.end_cursor = pagination_info['end_cursor']
        
        self.fetched_count += len(comments)
        
        return comments
    
    def get_max_comments(self):
        return self.max_comments
