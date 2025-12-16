"""
Quick fix script to convert Windows backslashes to forward slashes in FAISS metadata.
Run this once to fix existing index without re-indexing.
"""
import pickle
from pathlib import Path

# Paths
FAISS_INDEX_PATH = Path("data/faiss_index")
METADATA_FILE = FAISS_INDEX_PATH / "metadata.pkl"

print("=" * 60)
print("FAISS Metadata Path Fixer")
print("=" * 60)

# Load metadata
if not METADATA_FILE.exists():
    print(f"Error: Metadata file not found at {METADATA_FILE}")
    exit(1)

with open(METADATA_FILE, 'rb') as f:
    metadata = pickle.load(f)

print(f"\nLoaded {len(metadata)} metadata entries")

# Fix paths
fixed_count = 0
for item in metadata:
    if "image_path" in item:
        old_path = item["image_path"]
        new_path = old_path.replace("\\", "/")
        if old_path != new_path:
            item["image_path"] = new_path
            fixed_count += 1

print(f"Fixed {fixed_count} paths (converted \\ to /)")

# Save back
with open(METADATA_FILE, 'wb') as f:
    pickle.dump(metadata, f)

print(f"\n✓ Metadata saved to {METADATA_FILE}")
print("\nDone! Restart backend to use fixed paths.")
print("=" * 60)
