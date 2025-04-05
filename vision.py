import os
from google.cloud import vision_v1 as vision
from google.api_core.exceptions import GoogleAPICallError

def test_vision_api():
    """Test Google Vision API with detailed verification"""
    try:
        # 1. Verify Credentials
        creds_path = r"D:\GoogleApiKey\Service_Account_key.json"
        if not os.path.exists(creds_path):
            raise FileNotFoundError(f"Credential file not found at {creds_path}")
        
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path
        
        # 2. Test Client Initialization
        try:
            client = vision.ImageAnnotatorClient()
            print("✅ Client initialized successfully")
        except Exception as e:
            print(f"❌ Client initialization failed: {str(e)}")
            return

        # 3. Test Image Loading
        image_path = r"D:\AssigementMechanicsOfSearch\static\images\african-daisy-flower-nature-flora-41960.jpeg"
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found at {image_path}")
        
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        
        # 4. Test API Connection
        image = vision.Image(content=content)
        try:
            response = client.document_text_detection(image=image)
            
            # 5. Verify Response
            if response.error.message:
                print(f"❌ API Error: {response.error.message}")
            else:
                print("✅ API Connection successful")
                texts = response.text_annotations
                
                if texts:
                    print("\n📝 Detected Text:")
                    print(f"Primary text: {texts[0].description}")
                    print(f"\nDetails (first 3 items):")
                    for text in texts[1:4]:
                        print(f"- {text.description} (confidence: {text.confidence:.1%})")
                else:
                    print("ℹ️ No text detected in image")
                    
        except GoogleAPICallError as e:
            print(f"❌ API Call Failed: {str(e)}")

    except Exception as e:
        print(f"❌ Test Failed: {str(e)}")

if __name__ == "__main__":
    test_vision_api()