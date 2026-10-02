"""T4 deterministic, symmetric embedding (protocol §6).

Each text is lower-cased and split on non-alphanumeric characters. Each token is
hashed with SHA-256: the first four bytes choose one of 256 dimensions, and the
lowest bit of the fifth byte chooses the sign. Counts are L2-normalised. The same
function embeds queries and documents, so it is symmetric by construction; T4
therefore does not test query-versus-document embedding semantics (T2's question).
"""
import hashlib
import math
import re

DIMENSIONS = 256


def embed(text):
    vector = [0.0] * DIMENSIONS
    for token in re.split(r"[^a-z0-9]+", text.lower()):
        if not token:
            continue
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        dimension = int.from_bytes(digest[:4], "big") % DIMENSIONS
        vector[dimension] += 1.0 if digest[4] % 2 == 0 else -1.0
    norm = math.sqrt(sum(v * v for v in vector))
    return [v / norm for v in vector] if norm else vector
