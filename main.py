import argparse
import sys
from client import InstagramClient
from parser import InstagramParser
from paginator import InstagramPaginator, CommentsPaginator
from downloader import InstagramDownloader

def main():
    parser = argparse.ArgumentParser(description='Instagram Media Downloader (Python Version)')
    parser.add_argument('username', help='Instagram username to download posts from')
    parser.add_argument('--count', type=int, default=None, help='Number of images to download')
    parser.add_argument('--likes', action='store_true', help='Extract and display like counts')
    parser.add_argument('--comments', action='store_true', help='Extract and display comments')
    
    args = parser.parse_args()
    
    username = args.username
    max_count = args.count if args.count is not None else float('inf')
    
    print(f"Starting download for user: {username}")
    
    client = InstagramClient()
    insta_parser = InstagramParser()
    paginator = InstagramPaginator(client, insta_parser, username, max_count)
    downloader = InstagramDownloader(username)
    
    total_images_downloaded = 0
    total_posts_processed = 0
    
    try:
        for batch in paginator:
            for post in batch:
                print(f"\n--- Post {post['shortcode']} ---")
                if post['caption']:
                    print(f"Caption: {post['caption']}")
                
                if args.likes:
                    print(f"Likes: {post['like_count']:,}")
                
                if args.comments:
                    print(f"Total Comments: {post['comment_count']:,}")
                    print(f"Fetching comments for post {post['shortcode']}... (up to 50)")
                    comments_paginator = CommentsPaginator(client, insta_parser, post['post_id'], post['shortcode'])
                    comments = []
                    for batch in comments_paginator:
                        comments.extend(batch)
                    print(f"Fetched {min(len(comments), comments_paginator.get_max_comments())} comments.")
                    for i, comment in enumerate(comments[:comments_paginator.get_max_comments()]):
                        print(f"  @{comment['author']}: {comment['text'][:100]}{'...' if len(comment['text']) > 100 else ''}")

                for img in post['images']:
                    url = img['url']
                    filename = img['filename']
                    
                    print(f"Downloading image: {filename}... ", end='', flush=True)
                    if downloader.download_image(url, filename):
                        print("Done.")
                        total_images_downloaded += 1
                        paginator.update_count(1)
                    else:
                        print("Failed.")
                
                total_posts_processed += 1
                if total_posts_processed == max_count:
                    break
            
            if total_posts_processed == max_count:
                break
                
        print(f"\nFinished! Processed {total_posts_processed} posts, downloaded {total_images_downloaded} images to {username}/")
        
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
