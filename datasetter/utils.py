def doc_equal(doc1, doc2):
    """Test if two JSON-like documents are equel."""
    try:
        if isinstance(doc1, dict):
            assert isinstance(doc2, dict)
            for key in doc1.keys():
                assert key in doc2 and doc_equal(doc1[key], doc2[key])
        elif isinstance(doc1, list):
            assert isinstance(doc2, list) and len(doc1) == len(doc2)
            for x, y in zip(doc1, doc2):
                assert doc_equal(x, y)
        else:
            assert doc1 == doc2
        return True
    except AssertionError:
        return False
