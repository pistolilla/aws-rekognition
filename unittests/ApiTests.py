import sys, os, unittest, requests, json, re

# Ensuring consistency among modules
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)
sys.path.append(PARENT_DIR)

TEST_HOST = os.environ.get("TEST_HOST", "http://localhost")
TEST_PORT = os.environ.get("TEST_PORT", 5000)

TEST_URL = f"{TEST_HOST}:{TEST_PORT}"

testcases = [
    {
        "filename": "test1.jpeg",
        "labels": [
            ("Vehicle", 95), # format (label, minimum_confidence)
            ("Mustang", 85)
        ]
    },
    {
        "filename": "test2.png",
        "labels": [
            ("Family", 95),
            ("Clothing", 55)
        ]
    },
    {
        "filename": "test3.jpeg",
        "labels": [
            ("Bridge", 95),
            ("Ocean", 80)
        ]
    },
    {
        "filename": "test4.JPG",
        "labels": [
            ("Person", 95),
            ("Grass", 95)
        ]
    },
    {
        "filename": "test5.jpg",
        "labels": [
            ("Plant", 95),
            ("Fruit", 80)
        ]
    }
]

def get_labels_confidence(filename, unique=False):
    """ End-to-end file upload and recognition, for testing purposes only
    """
    filepath = os.path.join(os.path.join(THIS_DIR, "TestCases", filename))

    # 1. requesting presigned url
    url = f"{TEST_URL}/url" + (f"?filename={filename}" if not unique else "")
    r = requests.get(url)
    res = json.loads(r.text)

    # 2. uploading file
    with open(filepath, 'rb') as f:
        files = {'file': (filepath, f)}
        r = requests.post(res['url'], data=res['fields'], files=files)
        if not str(r.status_code).startswith("2"):
            raise Exception(f"Error {res.status_code} ({res.content})")

    # 3. reading labels
    r = requests.get(f"{TEST_URL}/labels?filename={res['fields']['key']}")
    response = json.loads(r.text)
    if not str(r.status_code).startswith("2"):
        return int(r.status_code), {}
    return int(r.status_code), {label["Name"]: label["Confidence"] for label in response["labels"]}

## testing if server is up
server_available = True
try:
    requests.get(f"{TEST_URL}/")
except: server_available = False

## test class for all api tests
class ApiTest(unittest.TestCase):
    ## basic api tests
    @unittest.skipUnless(server_available, "server is not running")
    def test1_url(self):
        r = requests.get(f"{TEST_URL}/url")
        self.assertTrue(int(r.status_code) == 200)
        res = json.loads(r.text)
        self.assertTrue(re.match(r"https://.*\.s3.amazonaws.com", res["url"]))
        self.assertTrue(re.match(r"^[-\w]{36}$", res["fields"]["key"]))

    @unittest.skipUnless(server_available, "server is not running")
    def test1_url_filename(self):
        r = requests.get(f"{TEST_URL}/url?filename=example")
        self.assertTrue(int(r.status_code) == 200)
        res = json.loads(r.text)
        self.assertTrue(re.match(r"https://.*\.s3.amazonaws.com", res["url"]))
        self.assertEqual("example", res["fields"]["key"])

    ## image upload and rekognition tests (end-to-end)
    @unittest.skipUnless(server_available, "server is not running")
    def test2_images(self):
        for testcase in testcases:
            print(f"Testing image: {testcase['filename']}")
            status_code, awslabels = get_labels_confidence(testcase["filename"], unique=False)
            self.assertGreaterEqual(status_code, 200)
            self.assertLess(status_code, 300)
            for label, confidence in testcase["labels"]:
                self.assertIn(label, awslabels)
                self.assertGreaterEqual(awslabels[label], confidence)

    @unittest.skipUnless(server_available, "server is not running")
    def test3_invalid_image(self):
        status_code, _ = get_labels_confidence("test6.txt", unique=False)
        self.assertGreaterEqual(status_code, 500)

### Run the tests
if __name__ == '__main__':
    unittest.main()