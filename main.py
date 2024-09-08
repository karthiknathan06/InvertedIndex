class InvertedIndex:
    def __init__(self):
        self.index = {
            'log_level': {},
            'message': {},
            'source_ip': {}
        }
        self.documents = {}

    def add_document(self, doc_id, document):
        self.documents[doc_id] = document
        for field, value in document.items():
            if field in self.index:
                terms = value.split() if isinstance(value, str) else [value]
                for term in terms:
                    if term not in self.index[field]:
                        self.index[field][term] = set()
                    self.index[field][term].add(doc_id)

    def search(self, queries):
        result_docs = set()
        for field, term in queries.items():
            if field in self.index and term in self.index[field]:
                if result_docs:
                    result_docs.intersection_update(self.index[field][term])
                else:
                    result_docs = self.index[field][term].copy()
        return [self.documents[doc_id] for doc_id in result_docs]

# Initialize the inverted index
inverted_index = InvertedIndex()

# Add documents
inverted_index.add_document(1, {
    "timestamp": "2024-09-08T10:00:00Z",
    "log_level": "ERROR",
    "message": "Database connection failed",
    "source_ip": "192.168.1.10"
})

inverted_index.add_document(2, {
    "timestamp": "2024-09-08T10:01:00Z",
    "log_level": "WARN",
    "message": "High memory usage detected",
    "source_ip": "192.168.1.20"
})

inverted_index.add_document(3, {
    "timestamp": "2024-09-08T10:02:00Z",
    "log_level": "INFO",
    "message": "User login successful",
    "source_ip": "192.168.1.10"
})

# Search for logs with log_level "ERROR" and message containing "Database"
query = {
    'log_level': 'ERROR',
    'message': 'Database'
}

results = inverted_index.search(query)

for result in results:
    print(result)
