from utils.text_utils import preprocess_text

def test_preprocess_text():
    text = "This is a sample text with some stopwords."
    processed_text = preprocess_text(text)
    assert processed_text == "sample text stopword"