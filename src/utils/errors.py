class VectorStoreNotLoaded(Exception):
    def __init__(self, message="vector store not loaded"):
        super().__init__(message)

class NotGithubDomain(Exception):
    def __init__(self, message="not a github domain"):
        super().__init__(message)