import copy
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from local_docs_policy import validate_local_config


class LocalPolicyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.config = {'environment': {
            'KUJO_RAG_API_HOST':'127.0.0.1', 'KUJO_RAG_API_ALLOW_NON_LOOPBACK':'false',
            'KUJO_RAG_API_AUTH_PROVIDER':'bearer', 'KUJO_RAG_API_BEARER_TOKEN':'test-only',
            'KUJO_RAG_API_RBAC_ENABLED':'true', 'KUJO_RAG_API_RBAC_DEFAULT_ROLE':'reader',
            'KUJO_RAG_EMBEDDING_PROVIDER':'hash', 'KUJO_RAG_VECTOR_BACKEND':'local_json',
            'KUJO_RAG_NAMESPACE':'docs',
            'KUJO_RAG_INDEX_PATH':str(self.root/'data/local-kujo-docs/index.json'),
            'KUJO_RAG_API_INGEST_ALLOWED_ROOTS':str(self.root/'data/local-kujo-docs/corpus'),
        }}

    def test_valid_local_service(self):
        self.assertEqual(validate_local_config(self.config,self.root)['KUJO_RAG_NAMESPACE'],'docs')

    def test_reject_exposure_and_privilege_changes(self):
        for key,value in [('API_HOST','0.0.0.0'),('API_ALLOW_NON_LOOPBACK','true'),('API_AUTH_PROVIDER','none'),('API_BEARER_TOKEN',''),('API_RBAC_ENABLED','false'),('API_RBAC_DEFAULT_ROLE','admin'),('API_CORS_ENABLED','true'),('API_RBAC_POLICY_JSON','{"reader":["admin"]}'),('EMBEDDING_PROVIDER','openai'),('VECTOR_BACKEND','qdrant'),('NAMESPACE','default'),('INDEX_PATH','/tmp/shared.json'),('API_INGEST_ALLOWED_ROOTS','/')]:
            with self.subTest(key=key):
                candidate=copy.deepcopy(self.config)
                candidate['environment']['KUJO_RAG_'+key]=value
                with self.assertRaises(ValueError):validate_local_config(candidate,self.root)

    def test_reject_competing_dotenv(self):
        (self.root/'.env').write_text('KUJO_RAG_API_AUTH_PROVIDER=none\n')
        with self.assertRaises(ValueError):validate_local_config(self.config,self.root)

    def test_reject_symlink_escape(self):
        data=self.root/'data/local-kujo-docs';data.mkdir(parents=True)
        outside=self.root/'outside';outside.mkdir()
        (data/'escape').symlink_to(outside,target_is_directory=True)
        self.config['environment']['KUJO_RAG_INDEX_PATH']=str(data/'escape/index.json')
        with self.assertRaises(ValueError):validate_local_config(self.config,self.root)


if __name__ == '__main__':unittest.main()
