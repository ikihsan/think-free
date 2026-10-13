"""Create a third evaluation harness structure for preflight adapter prototyping.

This harness uses a single JSONL file format, different from:
- modelscope/evalscope: two files (predictions + reviews) joined by `index`
- openai/evals: one append-only event stream joined by `sample_id`

Format: results.jsonl with one JSON object per line, each containing:
  - sample_id: stable identifier
  - model_output: the model's output
  - expected: the expected/ground-truth answer
  - correct: whether model_output matches expected
"""
import json
import os
import tempfile


def create_test_harness():
    """Create a test harness with a single JSONL output format."""
    tmpdir = tempfile.mkdtemp(prefix="preflight_test_")
    print(f"Test harness directory: {tmpdir}")

    # Create a single JSONL file harness structure
    jsonl_path = os.path.join(tmpdir, "results.jsonl")
    with open(jsonl_path, "w") as f:
        for i in range(20):
            entry = {
                "sample_id": f"sample_{i:03d}",
                "model_output": f"This is model output {i} with some content",
                "expected": f"This is the expected answer {i}",
                "correct": i < 15  # first 15 are "correct" (match), last 5 are incorrect
            }
            f.write(json.dumps(entry) + "\n")

    # Key directory with ground truth (for C1 concordance check)
    key_dir = os.path.join(tmpdir, "key")
    os.mkdir(key_dir)

    # Key file: mapping of sample_id to expected answer
    key_data = {}
    for i in range(20):
        key_data[f"sample_{i:03d}"] = f"expected_answer_{i}"

    key_path = os.path.join(key_dir, "ground_truth.jsonl")
    with open(key_path, "w") as f:
        for sample_id, expected in key_data.items():
            f.write(json.dumps({"sample_id": sample_id, "expected": expected}) + "\n")

    # Output directory with model results
    output_dir = os.path.join(tmpdir, "output")
    os.mkdir(output_dir)

    # Output file
    output_path = os.path.join(output_dir, "model_results.jsonl")
    with open(output_path, "w") as f:
        for i in range(20):
            if i < 15:
                model_out = f"This is model output {i} with some content"
            else:
                model_out = f"Wrong answer {i} - model hallucinated"
            entry = {
                "sample_id": f"sample_{i:03d}",
                "model_output": model_out,
                "expected": f"expected_answer_{i}"
            }
            f.write(json.dumps(entry) + "\n")

    print(f"\nCreated test harness with:")
    print(f"  JSONL file: {jsonl_path}")
    print(f"  Key file: {key_path}")
    print(f"  Output dir: {output_dir}")

    # Verify the files
    print("\nVerifying files...")
    for root, dirs, files in os.walk(tmpdir):
        for file in files:
            path = os.path.join(root, file)
            size = os.path.getsize(path)
            print(f"  {path} ({size} bytes)")

    print(f"\nTotal: 3 files created in {tmpdir}")
    return tmpdir


if __name__ == "__main__":
    harness_dir = create_test_harness()
    print(f"\nHarness directory: {harness_dir}")