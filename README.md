[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)

<!-- These are examples of badges you might also want to add to your README. Update the URLs accordingly.
[![Built Status](https://api.cirrus-ci.com/github/<USER>/youtube_analysis.svg?branch=main)](https://cirrus-ci.com/github/<USER>/youtube_analysis)
[![ReadTheDocs](https://readthedocs.org/projects/youtube_analysis/badge/?version=latest)](https://youtube_analysis.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/youtube_analysis/main.svg)](https://coveralls.io/r/<USER>/youtube_analysis)
[![PyPI-Server](https://img.shields.io/pypi/v/youtube_analysis.svg)](https://pypi.org/project/youtube_analysis/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/youtube_analysis.svg)](https://anaconda.org/conda-forge/youtube_analysis)
[![Monthly Downloads](https://pepy.tech/badge/youtube_analysis/month)](https://pepy.tech/project/youtube_analysis)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/youtube_analysis)
-->

# YouTube Comments Analysis

> Repository containing Python notebooks and scripts for YouTube comments analysis.

## Features

- **Pyscaffold Structure:** Organized and scalable project structure for easy update and extension.
- **Conda Environment:** Utilizes Conda for managing dependencies, ensuring reproducibility.
- **Notebooks:** Jupyter notebooks offering step-by-step workflow, including data collection, sentiment analysis and question anwsering.
- **Scripts:** Python scripts for data extraction, preprocessing, and statistical insights from YouTube comments.

## Getting Started

1. Clone the repository: 
`git clone https://github.com/abljoel/youtube-comments-analysis.git`
2. Create an environment `youtube_analysis` with the help of [conda]:
   ```
   conda env create -f youtube_analysis.yml
   ```
3. Activate the new environment with:
   ```
   conda activate youtube_analysis
   ```

4. For getting the project installed in editable mode for actively working on the code:
   ```
   pip install -e .
   ```

5. Explore the `notebooks` directory for step-by-step analyses.
6. Utilize the `scripts` directory for doing the work programmatically.
7. The `src/youtube_analysis` directory contains the main functionality.

## Notebooks

The notebooks follow numerical order to easily locate steps. The last one, `06-information-extraction-from-comments.ipynb`, contains the final analysis for insight extraction.

## Scripts

1. **data_collection.py:** Script for extracting YouTube comments data.
2. **data_preparation.py:** Prepare the data for analysis by cleaning text and extracting new features.
3. **insight_extraction.py:** Give summary of sentiment ratio and most frequent topics

#### Example Usages

1. **data_collection.py:**
    - Extract YouTube comments data.
    ```bash
    python data_collection.py --video_id YOUTUBE_VIDEO_ID --output_file comments_data.csv
    ```
    Replace `YOUTUBE_VIDEO_ID` with the actual video ID.

2. **data_preparation.py:**
    - Prepare data for analysis by cleaning text and extracting new features.
    ```bash
    python data_preparation.py --input_file comments_data.csv --output_file cleaned_features.pkl
    ```

3. **insight_extraction.py:**
    - Can generate a graph of sentiment ratio, identify most frequent topics, top author sentiments in number of comments, and plot engagement curve.
    ```bash
    python insight_extract.py --input_file cleaned_features.pkl --sentiment \
    --output_file sentiment_ratio.png
    ```
       
    ```bash
    python insight_extract.py --input_file cleaned_features.pkl --engagement \
    --output_file engagement_curves.png
    ```
    
    ```bash
    python insight_extract.py --input_file cleaned_features.pkl --top_viewer \
    --output_file topviewer_sentiments.png
    ```

    ```bash
    python insight_extract.py --input_file cleaned_features.pkl --top_topics 10 \
    --output_file topic_cloud.png
    ```


## License

This project is licensed under the MIT License - see the LICENSE.txt file for details.

<!-- pyscaffold-notes -->

## Note

This project has been set up using [PyScaffold] 4.5 and the [dsproject extension] 0.7.2.

[conda]: https://docs.conda.io/
[pre-commit]: https://pre-commit.com/
[Jupyter]: https://jupyter.org/
[nbstripout]: https://github.com/kynan/nbstripout
[Google style]: http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
[PyScaffold]: https://pyscaffold.org/
[dsproject extension]: https://github.com/pyscaffold/pyscaffoldext-dsproject
