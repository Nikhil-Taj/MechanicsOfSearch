import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import xml.etree.ElementTree as ET 

nltk.download('punkt')
nltk.download('stopwords')

class SearchEngineIndexer:
    def __init__(self, data_path):
        self.data_path = data_path
        self.documents = {}

    def preprocess_text(self, text):
        """ Tokenizes, removes punctuation, converts to lowercase, removes stopwords, and applies stemming. """
        text = text.lower() 
        text = re.sub(r'\W+', ' ', text)  
        tokens = word_tokenize(text) 
        stop_words = set(stopwords.words("english"))  
        stemmer = PorterStemmer()  
        processed_tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]
        return processed_tokens  

    def build_index(self):
        """ Reads and indexes documents from XML """
        with open(self.data_path, "r", encoding="utf-8") as file:
            xml_content = file.read()
        
        if not xml_content.strip().startswith("<?xml"):
            xml_content = f"<?xml version='1.0' encoding='UTF-8'?><ROOT>{xml_content}</ROOT>"
        else:
            xml_content = xml_content.replace('<?xml version="1.0" encoding="UTF-8"?>', '<?xml version="1.0" encoding="UTF-8"?><ROOT>', 1) + "</ROOT>"

        root = ET.fromstring(xml_content)

        for doc in root.findall("doc"):
            doc_id_element = doc.find("docno")
            text_element = doc.find("text")

            doc_id = doc_id_element.text.strip() if doc_id_element is not None else "UNKNOWN"

           
            if text_element is None or text_element.text is None:
                print(f" Warning: No <text> found for doc_id: {doc_id}. Skipping document.")
                continue  

            text = text_element.text.strip()
            self.documents[doc_id] = text

        print(" Indexing completed!")

# Run indexing test
if __name__ == "__main__":
    indexer = SearchEngineIndexer("data/cran.all.1400.xml")
    indexer.build_index()
