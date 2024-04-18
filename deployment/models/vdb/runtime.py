from mlserver import types
from mlserver.model import MLModel
from mlserver.codecs import NumpyCodec, StringCodec
from mlserver.types import InferenceRequest, InferenceResponse
from qdrant_client import QdrantClient
from mlserver.logging import logger
from qdrant_client.models import Distance, VectorParams


def get_namespace():
    with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", mode="r") as f:
        return f.read()


class SearchQdrant(MLModel):#
    namespace = get_namespace()

    async def load(self) -> bool:
        qdrant_uri = f'qdrant-release.{get_namespace()}.svc.cluster.local'
        self.db_client = QdrantClient(host=qdrant_uri, port=6333)
        collections = self.db_client.get_collections()
        if not collections:
            self.db_client.recreate_collection(
                collection_name="seldon_core_v2_docs",
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
            )

        logger.info(f"---- loaded collection = {self.db_client.get_collections()} ----")
        logger.info(f"---- with {self.db_client.count(collection_name='seldon_core_v2_docs')} items----")

        self.ready = True
        return self.ready

    def unpack_input(self, payload: InferenceRequest):
        request_data = {}
        for inp in payload.inputs:
            if inp.name == 'output':
                request_data[inp.name] = (
                    NumpyCodec
                    .decode_input(inp)
                    .flatten()
                    .tolist()
                )
            elif inp.name == 'input':
                request_data[inp.name] = StringCodec.decode_input(inp)
        return request_data
    

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        query = self.unpack_input(payload)

        hits = self.db_client.search(
            collection_name="seldon_core_v2_docs",
            query_vector=query['output'],
            limit=2
        )

        context = ""
        for hit in hits:
            context += hit.payload['text']
            context += "\n\n"
    
        logger.info(f"context: {context}")

        return InferenceResponse(
            id=payload.id,
            model_name=self.name,
            model_version=self.version,
            outputs=[
                StringCodec.encode_output("context", [context])
            ],
        )
