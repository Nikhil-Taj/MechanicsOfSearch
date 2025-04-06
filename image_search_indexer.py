import re
import nltk
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import json

# Ensure NLTK data is available
nltk_data_dir = '/opt/render/project/src/nltk_data'
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir)
    nltk.download('punkt', download_dir=nltk_data_dir)
nltk.data.path.append(nltk_data_dir)

class SearchEngineIndexer:
    def __init__(self, data_path):
        self.data_path = data_path
        self.documents = {}

    def preprocess_text(self, text):
   
        # Convert text to lowercase
        text = text.lower()

        # Remove non-alphanumeric characters (including punctuation) using regex
        text = re.sub(r'[^a-z0-9\s]', '', text)

    # Tokenize the text into words
        tokens = word_tokenize(text)

    # Define stopwords and stemmer
        stop_words = set(stopwords.words("english"))
        stemmer = PorterStemmer()

    # Remove stopwords and apply stemming
        processed_tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]

        return processed_tokens


    def load_image_data(self):
        """Load image data from a JSON file."""
        with open(self.data_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def build_index(self):
        """ Reads and indexes images from JSON file. """
        image_data = self.load_image_data()

        # Debugging line: check the content of the image data loaded
        print(f"Image Data: {image_data[:5]}")  # Print first 5 records for inspection

        for image in image_data:
            try:
                description = image['description']  # Textual surrogate (description) of the image
                image_url = image.get('url')  # Using .get() to avoid KeyError
                
                if image_url is None:  # Check if the URL is missing
                    print(f"Warning: Missing URL for image with description: {description}")
                    continue  # Skip this image if URL is missing

                # Debugging line: check each description being indexed
                print(f"Indexing image with URL: {image_url} and description: {description}")
                self.documents[image_url] = self.preprocess_text(description)

            except KeyError as e:
                print(f"Error: Missing key {e} in image data")
                continue  # Skip this image if a KeyError is encountered

        print(f"Indexed data: {self.documents}")  # Debugging line
        print("Indexing completed!")

    def search(self, query):
        query_tokens = self.preprocess_text(query)
        results = []
        for doc_id, doc_tokens in self.documents.items():
            # Count matching tokens
            score = sum(1 for token in query_tokens if token in doc_tokens)
            if score > 0:
                results.append((doc_id, score))
        
        # Sort by score (highest first)
        results.sort(key=lambda x: x[1], reverse=True)
        return [doc_id for doc_id, score in results]

if __name__ == "__main__":
    indexer = SearchEngineIndexer("image_data.json")  # Make sure to use the correct path for your JSON file
    indexer.build_index()

    # Example search query
    query = "forest"
    result = indexer.search(query)
    print(f"Search results for '{query}': {result}")
