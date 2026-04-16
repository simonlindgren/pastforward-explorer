"""One-time data preparation: copy files, pre-compute UMAP and position maps.

Run from the dashboard directory:
    python prepare_data.py
"""

import json
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from umap import UMAP

SRC = Path(__file__).parent.parent  # pf-facebook-analysis/
DATA_DIR = Path(__file__).parent / "data"
COUNTRIES = ["DK", "FI", "NO", "SE"]


def copy_source_files():
    """Copy required data files into dashboard/data/."""
    DATA_DIR.mkdir(exist_ok=True)

    copies = {
        SRC / "2026-02-26" / "word2vec_similarities.json": DATA_DIR / "word2vec_similarities.json",
        SRC / "dictionary-terms.csv": DATA_DIR / "dictionary-terms.csv",
        SRC / "dictionary-terms-flat.csv": DATA_DIR / "dictionary-terms-flat.csv",
        SRC / "pf-filtered-posts.json": DATA_DIR / "pf-filtered-posts.json",
        SRC / "2026-02-26" / "table4_account_detail.csv": DATA_DIR / "table4_account_detail.csv",
    }
    for src_path, dst_path in copies.items():
        if src_path.exists():
            shutil.copy2(src_path, dst_path)
            print(f"  Copied {src_path.name}")
        else:
            print(f"  WARNING: {src_path} not found")

    # Copy models
    for cc in COUNTRIES:
        src = SRC / "2026-02-26" / f"w2v_{cc}.model"
        dst = DATA_DIR / f"w2v_{cc}.model"
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  Copied w2v_{cc}.model")


def compute_umap_projections():
    """Pre-compute 3D UMAP projections for each country's model."""
    import time

    print("\nComputing UMAP projections...")
    all_projections = {}

    for cc in COUNTRIES:
        model_path = DATA_DIR / f"w2v_{cc}.model"
        if not model_path.exists():
            print(f"  Skipping {cc}: model not found")
            continue

        model = Word2Vec.load(str(model_path))
        words = list(model.wv.key_to_index.keys())
        vectors = np.array([model.wv[w] for w in words])

        print(f"  {cc}: {len(words)} words, running UMAP...")
        t0 = time.time()
        reducer = UMAP(n_components=3, random_state=42, n_neighbors=15, min_dist=0.1)
        coords_3d = reducer.fit_transform(vectors)
        elapsed = time.time() - t0

        all_projections[cc] = {
            "words": words,
            "x": coords_3d[:, 0].tolist(),
            "y": coords_3d[:, 1].tolist(),
            "z": coords_3d[:, 2].tolist(),
        }
        print(f"  {cc}: done in {elapsed:.1f}s")

    out_path = DATA_DIR / "umap_3d.json"
    with open(out_path, "w") as f:
        json.dump(all_projections, f)
    print(f"  Saved to {out_path}")


def compute_word_positions():
    """For each word in filtered posts, count occurrences by political position.

    Posts already have a 'country' field. We use table4_account_detail.csv
    to map account name -> Position.  The 'Account' column matches the
    post's user.name field (display name), which gives much better coverage
    than the pageName slug.
    """
    print("\nComputing word-position counts...")

    posts_path = DATA_DIR / "pf-filtered-posts.json"
    detail_path = DATA_DIR / "table4_account_detail.csv"

    with open(posts_path) as f:
        posts = json.load(f)

    detail = pd.read_csv(detail_path)
    # Build position lookup: prefer user.name (display name) over pageName slug
    account_to_position = dict(zip(detail["Account"], detail["Position"]))

    result = {}
    for cc in COUNTRIES:
        country_posts = [p for p in posts if p.get("country") == cc]
        word_pos = defaultdict(lambda: Counter())
        matched_posts = 0

        for post in country_posts:
            user_name = (post.get("user") or {}).get("name", "")
            position = account_to_position.get(user_name)
            if not position:
                # Fallback: try pageName slug
                position = account_to_position.get(post.get("pageName", ""))
            if not position:
                continue
            matched_posts += 1
            text = post.get("text", "") or ""
            words = re.findall(r"\b\w+\b", text.lower())
            words = [w for w in words if len(w) > 2]
            for w in words:
                word_pos[w][position] += 1

        result[cc] = {w: dict(counts) for w, counts in word_pos.items()}
        print(f"  {cc}: {len(result[cc])} words mapped ({matched_posts}/{len(country_posts)} posts matched)")

    out_path = DATA_DIR / "word_positions.json"
    with open(out_path, "w") as f:
        json.dump(result, f)
    print(f"  Saved to {out_path}")


if __name__ == "__main__":
    print("=== PastForward Dashboard Data Preparation ===\n")
    print("Copying source files...")
    copy_source_files()
    compute_umap_projections()
    compute_word_positions()
    print("\n=== Done! ===")
