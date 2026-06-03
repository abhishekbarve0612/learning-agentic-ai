import numpy as np
from corpus import DOCS, CHUNKS

def get_embedder():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    cos(theta) = (a.b) / (||a|| * ||b||)
    Only the direction of vectors matters not the magnitude(length of vectors)
    """
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    """
    Straight line distance.
    Magnitude-sensitive: two vectors pointing the same way but with different lengths are 'far', Smaller = 'closer'
    """
    return float(np.sqrt(np.sum((a - b) ** 2)))

def top_k_cosine(query_vec, doc_vecs, k = 3):
    scores = [cosine_similarity(query_vec, d) for d in doc_vecs]
    order = np.argsort(scores)[::-1][:k]

    return [(int(i), scores[int(i)]) for i in order]

def top_k_by_euclidean(query_vec, doc_vecs, k = 3):
    dists = [euclidean_distance(query_vec, d) for d in doc_vecs]
    order = np.argsort(dists)[:k]

    return [(int(i), dists[int(i)]) for i in order]

def main():

    model = get_embedder()

    doc_vecs = np.array(model.encode(DOCS), dtype="float32")

    print(f"Embedded {len(DOCS)} chunks. Each vector has {doc_vecs.shape[1]} dimensions.")

    print("An embedding is literally this many floats: ", doc_vecs[0][:8], "...\n")

    query = "What port does the Helios server listen on?"

    q = np.array(model.encode([query]), dtype="float32")[0]

    print(f"Query: {query} \n")

    print("Top-3 by COSINE (direction only):")


    for i, s in top_k_cosine(q, doc_vecs):
        print(f" [{i}] dist={s:.4f} {CHUNKS[i][:70]}...")

    print("\nTop-3 by EUCLIDEAN (distance matters):")
    
    for i, d in top_k_by_euclidean(q, doc_vecs):
        print(f" [{i}] dist={d:.4f} {CHUNKS[i][:70]}...")

    def normalize(v):
        return v / np.linalg.norm(v)

    a, b = doc_vecs[1], doc_vecs[3]
    cos = cosine_similarity(a, b)
    dot_normalized = float(np.dot(normalize(a), normalize(b)))

    print("\nCosine(a,b)             =", round(cos, 6))

    print("Dot(normalize(a),norm(b)) =", round(dot_normalized, 6))
    print("Equal (within float error)?", np.isclose(cos, dot_normalized))
    print(
        "\nThat's why most vector DBs ask you to normalize and then use inner "
        "product:\nit's the same ranking as cosine but cheaper to compute."
    )


if __name__ == "__main__":
    main()

'''

Output

Embedded 10 chunks. Each vector has 384 dimensions.
An embedding is literally this many floats:  [-0.0543636   0.0546773  -0.14682797 -0.03594044 -0.03586206 -0.05902696
 -0.00374913 -0.02025951] ...

Query: What port does the Helios server listen on? 

Top-3 by COSINE (direction only):
 [1] dist=0.7997 The Helios daemon listens on port 7330 by default. You can change it w...
 [5] dist=0.5633 Helios supports three source connectors out of the box: Apache Kafka, ...
 [0] dist=0.5437 Helios is a stream-processing command-line tool built by the (fictiona...

Top-3 by EUCLIDEAN (distance matters):
 [1] dist=0.6330 The Helios daemon listens on port 7330 by default. You can change it w...
 [5] dist=0.9345 Helios supports three source connectors out of the box: Apache Kafka, ...
 [0] dist=0.9554 Helios is a stream-processing command-line tool built by the (fictiona...

Cosine(a,b)             = 0.481537
Dot(normalize(a),norm(b)) = 0.481537
Equal (within float error)? True

That's why most vector DBs ask you to normalize and then use inner product:
it's the same ranking as cosine but cheaper to compute.


'''