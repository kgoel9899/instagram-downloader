import requests
import json
from constants import GRAPHQL_URL, DEFAULT_HEADERS

class InstagramClient:
    
    def __init__(self):
        self.headers = DEFAULT_HEADERS

    def fetch_batch(self, username, after=None):
        variables = {
            "after": after,
            "before": None,
            "data": {
                "count": 12,
                "include_reel_media_seen_timestamp": True,
                "include_relationship_info": True,
                "latest_besties_reel_media": True,
                "latest_reel_media": True
            },
            "first": 12,
            "last": None,
            "username": username
        }

        data = {
            'variables': json.dumps(variables),
            'doc_id': '25855331814139230'
        }

        try:
            headers = self.headers.copy()
            headers['content-type'] = 'application/x-www-form-urlencoded'
            
            response = requests.post(GRAPHQL_URL, data=data, headers=headers)
            response.raise_for_status()
            res_json = response.json()
            return res_json['data']['xdt_api__v1__feed__user_timeline_graphql_connection']
        except Exception as e:
            print(f"Error fetching batch: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response status: {e.response.status_code}")
            raise e

    def fetch_comments(self, media_id, shortcode, after=None):
        """
        Fetches a batch of comments for a specific media ID
        """
        variables = {
            'media_id': media_id,
            '__relay_internal__pv__PolarisIsLoggedInrelayprovider': True
        }
        
        doc_id = '26103263252639102'
        
        if after:
            variables.update({
                'after': after,
                'before': None,
                'first': 10,
                'last': None,
                'sort_order': 'popular'
            })
            doc_id = '26224338453892885'

        data = {
            'variables': json.dumps(variables),
            'doc_id': doc_id
        }

        try:
            headers = self.headers.copy()
            headers['referer'] = f'https://www.instagram.com/p/{shortcode}/'
            headers['accept-encoding'] = 'identity'
            response = requests.post(GRAPHQL_URL, data=data, headers=headers)
            response.raise_for_status()
            res_json = response.json()
            return res_json['data']['xdt_api__v1__media__media_id__comments__connection']
        except Exception as e:
            print(f"Error fetching comments: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response status: {e.response.status_code}")
            raise e