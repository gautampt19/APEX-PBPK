import sys
from extract_pbpk_params import extract_pbpk_parameters
extract_pbpk_parameters(
    md_file_path="pipeline_output/s12249-023-02680-y_cleaned.md",
    output_json_path="test.json",
    model_extract="gemma4:31b",
    model_generate="muse-glimmer",
    backend="ollama",
    image_dir="ocr_output/s12249-023-02680-y"
)
