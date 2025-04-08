class PyAPSuiteError(Exception):
    """Base exception for this module"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)