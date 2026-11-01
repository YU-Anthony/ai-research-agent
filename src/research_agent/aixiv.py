"""Optional fail-closed aiXiv adapter.

No endpoint has been verified against official documentation in this environment.
Do not guess API routes, authentication schemes, or submission payloads.
"""
import os


class AiXivClient:
    def __init__(self):
        self._token = os.environ.get('AIXIV_TOKEN')

    @property
    def credential_present(self):
        return bool(self._token)

    def submit(self, manuscript, *, human_approved=False):
        if not human_approved:
            raise PermissionError('Explicit human approval is required for submission')
        raise NotImplementedError('aiXiv endpoints and authentication must first be verified against official documentation')

    def post_discussion(self, text, *, human_approved=False):
        if not human_approved:
            raise PermissionError('Explicit human approval is required for posting')
        raise NotImplementedError('aiXiv discussion API is unverified and disabled')
