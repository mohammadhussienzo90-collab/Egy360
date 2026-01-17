# core/mailchimp_integration.py
"""
Mailchimp Integration for Egy360 Newsletter

This module handles syncing newsletter subscribers to Mailchimp
for email marketing campaigns.

Setup:
1. Create a Mailchimp account at https://mailchimp.com (free up to 500 contacts)
2. Get your API key: Account > Extras > API keys
3. Find your Audience ID: Audience > Settings > Audience name and defaults
4. Add to environment variables:
   - MAILCHIMP_API_KEY
   - MAILCHIMP_AUDIENCE_ID
   - MAILCHIMP_SERVER_PREFIX (e.g., 'us21' from your API key)
"""

import requests
import logging
import hashlib
from django.conf import settings

logger = logging.getLogger(__name__)


class MailchimpClient:
    """
    Mailchimp API client for managing newsletter subscribers.

    Uses Mailchimp Marketing API v3.
    Documentation: https://mailchimp.com/developer/marketing/api/
    """

    def __init__(self):
        """Initialize Mailchimp client with credentials from settings."""
        self.api_key = getattr(settings, 'MAILCHIMP_API_KEY', '')
        self.audience_id = getattr(settings, 'MAILCHIMP_AUDIENCE_ID', '')
        self.server_prefix = getattr(settings, 'MAILCHIMP_SERVER_PREFIX', '')

        if self.api_key and '-' in self.api_key:
            # Extract server prefix from API key (format: key-usXX)
            self.server_prefix = self.api_key.split('-')[-1]

        self.base_url = f"https://{self.server_prefix}.api.mailchimp.com/3.0"

    def is_configured(self):
        """Check if Mailchimp is properly configured."""
        return bool(self.api_key and self.audience_id and self.server_prefix)

    def _get_subscriber_hash(self, email):
        """
        Get MD5 hash of lowercase email for Mailchimp API.

        Mailchimp uses this hash as the subscriber identifier.
        """
        return hashlib.md5(email.lower().encode()).hexdigest()

    def _make_request(self, method, endpoint, data=None):
        """
        Make authenticated request to Mailchimp API.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            endpoint: API endpoint (e.g., '/lists/{list_id}/members')
            data: Optional JSON data for request body

        Returns:
            dict: Response data or error information
        """
        if not self.is_configured():
            return {'success': False, 'error': 'Mailchimp not configured'}

        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.request(
                method,
                url,
                json=data,
                auth=('anystring', self.api_key),
                timeout=30
            )

            if response.status_code in [200, 201]:
                return {'success': True, 'data': response.json()}
            elif response.status_code == 400:
                error_data = response.json()
                return {
                    'success': False,
                    'error': error_data.get('detail', 'Bad request'),
                    'title': error_data.get('title', '')
                }
            else:
                return {
                    'success': False,
                    'error': f'API error: {response.status_code}'
                }

        except requests.RequestException as e:
            logger.error(f"Mailchimp API error: {e}")
            return {'success': False, 'error': str(e)}

    def add_subscriber(self, email, first_name='', last_name='', tags=None):
        """
        Add a new subscriber to the Mailchimp audience.

        Args:
            email: Subscriber email address
            first_name: Optional first name
            last_name: Optional last name
            tags: Optional list of tags (e.g., ['newsletter', 'website'])

        Returns:
            dict: Success status and subscriber data or error
        """
        if tags is None:
            tags = ['newsletter', 'website-signup']

        data = {
            'email_address': email.lower(),
            'status': 'subscribed',  # Use 'pending' for double opt-in
            'merge_fields': {
                'FNAME': first_name,
                'LNAME': last_name,
            },
            'tags': tags,
            'source': 'Egy360 Website'
        }

        endpoint = f"/lists/{self.audience_id}/members"
        result = self._make_request('POST', endpoint, data)

        if result['success']:
            logger.info(f"Added subscriber to Mailchimp: {email}")
        elif 'already a list member' in result.get('error', '').lower():
            # Subscriber already exists - not an error
            logger.info(f"Subscriber already exists in Mailchimp: {email}")
            result['success'] = True
            result['already_subscribed'] = True
        else:
            logger.warning(f"Failed to add subscriber to Mailchimp: {email} - {result.get('error')}")

        return result

    def update_subscriber(self, email, first_name=None, last_name=None, tags=None):
        """
        Update an existing subscriber's information.

        Args:
            email: Subscriber email address
            first_name: New first name (optional)
            last_name: New last name (optional)
            tags: New tags to add (optional)

        Returns:
            dict: Success status and updated data or error
        """
        subscriber_hash = self._get_subscriber_hash(email)

        data = {}
        if first_name is not None or last_name is not None:
            data['merge_fields'] = {}
            if first_name:
                data['merge_fields']['FNAME'] = first_name
            if last_name:
                data['merge_fields']['LNAME'] = last_name

        endpoint = f"/lists/{self.audience_id}/members/{subscriber_hash}"
        return self._make_request('PATCH', endpoint, data)

    def unsubscribe(self, email):
        """
        Unsubscribe a member from the audience.

        Args:
            email: Subscriber email address

        Returns:
            dict: Success status or error
        """
        subscriber_hash = self._get_subscriber_hash(email)

        data = {'status': 'unsubscribed'}

        endpoint = f"/lists/{self.audience_id}/members/{subscriber_hash}"
        return self._make_request('PATCH', endpoint, data)

    def get_subscriber(self, email):
        """
        Get subscriber information.

        Args:
            email: Subscriber email address

        Returns:
            dict: Subscriber data or error
        """
        subscriber_hash = self._get_subscriber_hash(email)
        endpoint = f"/lists/{self.audience_id}/members/{subscriber_hash}"
        return self._make_request('GET', endpoint)

    def add_tags(self, email, tags):
        """
        Add tags to a subscriber.

        Args:
            email: Subscriber email address
            tags: List of tag names to add

        Returns:
            dict: Success status or error
        """
        subscriber_hash = self._get_subscriber_hash(email)

        data = {
            'tags': [{'name': tag, 'status': 'active'} for tag in tags]
        }

        endpoint = f"/lists/{self.audience_id}/members/{subscriber_hash}/tags"
        return self._make_request('POST', endpoint, data)

    def get_audience_stats(self):
        """
        Get audience statistics (total subscribers, etc.).

        Returns:
            dict: Audience statistics or error
        """
        endpoint = f"/lists/{self.audience_id}"
        return self._make_request('GET', endpoint)


# Singleton instance
mailchimp_client = MailchimpClient()


def sync_subscriber_to_mailchimp(email, name=''):
    """
    Convenience function to sync a subscriber to Mailchimp.

    Called from newsletter_subscribe view after saving to database.

    Args:
        email: Subscriber email
        name: Full name (will be split into first/last)

    Returns:
        bool: True if successful or Mailchimp not configured
    """
    if not mailchimp_client.is_configured():
        logger.debug("Mailchimp not configured, skipping sync")
        return True  # Return True so it doesn't block the subscription

    # Split name into first and last
    parts = name.split(' ', 1) if name else ['', '']
    first_name = parts[0]
    last_name = parts[1] if len(parts) > 1 else ''

    result = mailchimp_client.add_subscriber(
        email=email,
        first_name=first_name,
        last_name=last_name,
        tags=['newsletter', 'egypt-travel']
    )

    return result.get('success', False)
