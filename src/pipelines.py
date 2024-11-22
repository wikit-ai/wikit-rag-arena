import requests


class BasePipeline:
    """Base class for RAG (Retrieval-Augmented Generation) pipelines."""
    def __init__(self):
        self.name = "Base Pipeline"
        self.url = "http://httpbin.org/anything"

    def generate(self, query: str):
        """Makes a POST request to the pipeline endpoint with the given query.
        
        Args:
            query (str): The input text to process
            
        Returns:
            dict: JSON response from the pipeline
            
        Raises:
            Exception: If the request fails
        """
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        data = {"utterance": query}

        response = requests.post(self.url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Request failed [Pipeline:{self.name}][Status Code:{response.status_code}]"
            )


class GraphRagPipeline(BasePipeline):
    """Pipeline for graph-based RAG processing"""
    def __init__(self):
        self.name = "GraphRAG"
        self.url = "https://api-kg-rag-preprod.staging.wikit.ai/api/graph-rag/invoke"


class KgRagPipeline(BasePipeline):
    """Pipeline for knowledge graph-based RAG processing"""
    def __init__(self):
        self.name = "KG-RAG"
        self.url = "https://api-kg-rag-preprod.staging.wikit.ai/api/kg-rag/invoke"


class TextRagPipeline(BasePipeline):
    """Pipeline for text-based RAG processing"""
    def __init__(self):
        self.name = "Text-RAG"
        self.url = "https://api-kg-rag-preprod.staging.wikit.ai/api/text-rag/invoke"
