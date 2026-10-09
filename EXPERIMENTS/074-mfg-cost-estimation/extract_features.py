#!/usr/bin/env python3
"""
Feature extractor for manufacturing cost estimation.
Reads synthetic JSON fixtures and extracts feature vectors.
Stdlib only.
"""

import json
import math
from pathlib import Path
from typing import Dict, List, Any


def extract_features(part: Dict[str, Any]) -> Dict[str, float]:
    """
    Extract numerical features from a part description.
    These are the inputs to the cost model.
    """
    features = {}
    envelope = part["envelope_mm"]
    stock = part["stock_mm"]
    material = part["material"]
    feats = part["features"]

    # Envelope features
    features["envelope_volume"] = envelope["width"] * envelope["depth"] * envelope["height"]
    features["envelope_surface_area"] = 2 * (
        envelope["width"] * envelope["depth"] +
        envelope["width"] * envelope["height"] +
        envelope["depth"] * envelope["height"]
    )
    features["envelope_max_dim"] = max(envelope.values())
    features["envelope_aspect_ratio"] = max(envelope.values()) / min(envelope.values())

    # Stock features
    features["stock_volume"] = stock["width"] * stock["depth"] * stock["height"]
    features["stock_margin_ratio"] = features["stock_volume"] / features["envelope_volume"]

    # Material features (one-hot encoded)
    for mat in ["6061_aluminum", "304_stainless", "mild_steel", "abs_plastic"]:
        features[f"material_{mat}"] = 1.0 if material == mat else 0.0

    # Feature counts and aggregates
    feat_counts = {}
    feat_volumes = {}
    feat_lengths = {}

    for f in feats:
        ftype = f["type"]
        feat_counts[ftype] = feat_counts.get(ftype, 0) + 1

        if ftype == "pocket":
            vol = f["width"] * f["depth"] * f["height"]
            feat_volumes[ftype] = feat_volumes.get(ftype, 0) + vol
        elif ftype == "hole":
            vol = math.pi * (f["diameter"]/2)**2 * f["depth"]
            feat_volumes[ftype] = feat_volumes.get(ftype, 0) + vol
        elif ftype == "counterbore":
            vol = math.pi * (f["cb_dia"]/2)**2 * f["cb_depth"]
            feat_volumes[ftype] = feat_volumes.get(ftype, 0) + vol
        elif ftype == "bend":
            feat_lengths[ftype] = feat_lengths.get(ftype, 0) + f["length"]
        elif ftype == "thread":
            # Approximate thread engagement length
            feat_lengths[ftype] = feat_lengths.get(ftype, 0) + f["depth"]
        elif ftype == "chamfer":
            feat_lengths[ftype] = feat_lengths.get(ftype, 0) + f["length"] * f["width"]

    # Feature count features
    for ftype in ["pocket", "hole", "bend", "thread", "counterbore", "chamfer"]:
        features[f"count_{ftype}"] = float(feat_counts.get(ftype, 0))
        features[f"volume_{ftype}"] = feat_volumes.get(ftype, 0.0)
        features[f"length_{ftype}"] = feat_lengths.get(ftype, 0.0)

    # Derived features
    features["total_features"] = float(len(feats))
    features["total_machining_volume"] = sum(v for k, v in feat_volumes.items())
    features["total_bend_length"] = feat_lengths.get("bend", 0.0)
    features["total_thread_length"] = feat_lengths.get("thread", 0.0)

    # Complexity indicators
    features["has_bends"] = 1.0 if feat_counts.get("bend", 0) > 0 else 0.0
    features["has_threads"] = 1.0 if feat_counts.get("thread", 0) > 0 else 0.0
    features["has_pockets"] = 1.0 if feat_counts.get("pocket", 0) > 0 else 0.0

    return features


def load_split(split: str) -> List[Dict[str, Any]]:
    """Load a split from fixtures."""
    path = Path(__file__).parent / "fixtures" / f"{split}.jsonl"
    parts = []
    with open(path) as f:
        for line in f:
            parts.append(json.loads(line))
    return parts


def save_features(split: str, feature_data: List[Dict[str, Any]]):
    """Save extracted features."""
    path = Path(__file__).parent / "fixtures" / f"{split}_features.jsonl"
    with open(path, "w") as f:
        for item in feature_data:
            f.write(json.dumps(item) + "\n")


def main():
    for split in ["train", "val", "test"]:
        parts = load_split(split)
        feature_data = []

        for part in parts:
            feats = extract_features(part)
            feature_data.append({
                "id": part["id"],
                "split": split,
                "ground_truth_cost": part["ground_truth_cost"],
                "features": feats,
            })

        save_features(split, feature_data)
        print(f"{split}: extracted features for {len(feature_data)} parts")

    # Print feature summary for train
    train_data = load_split("train")
    sample_feats = extract_features(train_data[0])
    print(f"\nFeature vector dimension: {len(sample_feats)}")
    print(f"Sample features: {list(sample_feats.keys())}")


if __name__ == "__main__":
    main()