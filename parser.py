class InstagramParser:
    @staticmethod
    def extract_media(batch_data):
        """
        Extracts image URLs, filenames, and metadata from the batch data.
        Returns a list of dictionaries representing posts.
        """
        posts = []
        edges = batch_data.get('edges', [])
        
        for edge in edges:
            node = edge.get('node', {})
            if not node:
                continue
                
            post_id = node.get('pk')
            shortcode = node.get('code')
            
            metadata = {
                'post_id': post_id,
                'shortcode': shortcode,
                'like_count': node.get('like_count'),
                'comment_count': node.get('comment_count'),
                'caption': node.get('caption', {}).get('text') if node.get('caption') else None,
                'timestamp': node.get('taken_at'),
                'images': []
            }
            
            # Identify all media items in the post (single image/video or carousel)
            carousel_media = node.get('carousel_media')
            media_items = carousel_media if carousel_media else [node]
            
            for i, item in enumerate(media_items):
                # Skip videos (media_type 2)
                if item.get('media_type') == 2:
                    continue
                
                image_versions = item.get('image_versions2', {})
                candidates = image_versions.get('candidates', [])
                
                if candidates:
                    # Get the best quality image (usually the first one)
                    image_url = candidates[0].get('url')
                    # Use a suffix for carousel items
                    filename = f"{shortcode}_{i + 1}.jpg" if len(media_items) > 1 else f"{shortcode}.jpg"
                    metadata['images'].append({
                        'url': image_url,
                        'filename': filename
                    })
            
            if metadata['images']:
                posts.append(metadata)
        
        return posts

    @staticmethod
    def extract_comments(comment_data):
        if not comment_data:
            return []
            
        comments = []
        
        edges = comment_data['edges']
        for edge in edges:
            node = edge.get('node', {})
            comments.append({
                'author': node.get('user', {}).get('username'),
                'text': node.get('text'),
                'timestamp': node.get('created_at')
            })
        return comments

    @staticmethod
    def get_pagination_info(batch_data):
        page_info = batch_data.get('page_info', {})
        return {
            'has_next_page': page_info.get('has_next_page', False),
            'end_cursor': page_info.get('end_cursor')
        }

    @staticmethod
    def get_comments_pagination_info(comment_data):
        page_info = comment_data.get('page_info', {})
        return {
            'has_next_page': page_info.get('has_next_page', False),
            'end_cursor': page_info.get('end_cursor')
        }
