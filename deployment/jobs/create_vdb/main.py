import json
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct


def get_namespace():
    with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", mode="r") as f:
        return f.read()


if __name__ == '__main__':
    import json
    with open('vectorized-docs.json', 'r') as f:
        items = json.load(f)

    uri = f'qdrant-release.{get_namespace()}.svc.cluster.local'

    client = QdrantClient(host=uri, port=6333, timeout=60)
    client.recreate_collection(
        collection_name="seldon_core_v2_docs",
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
    )

    ind = 0
    chunk_size = 10
    while items[ind:ind+chunk_size]:
        to_insert = items[ind:ind+chunk_size]
        client.upsert(
            collection_name="seldon_core_v2_docs", 
            points=[
                PointStruct(
                    id=item['key'],
                    vector=item['embedding'],
                    payload={
                        'text': item['text'],
                        'meta': item['meta'],
                        'page': item['page'],
                        'section': item['section']
                    }
                )
                for item in to_insert
            ]
        )
        print(f"---- Inserted chunk: {ind} -> {ind + chunk_size} ----")    
        ind += chunk_size

    print(f"---- loaded collection = {client.get_collections()} ----")
    print(f"---- with {client.count(collection_name='seldon_core_v2_docs')} items----")