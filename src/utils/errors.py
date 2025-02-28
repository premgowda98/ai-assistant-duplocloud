class VectorStoreNotLoaded(Exception):
    def __init__(self, message="vector store not loaded"):
        super().__init__(message)