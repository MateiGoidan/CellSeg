# Data

This project uses the Clinical Microscopy Dataset introduced in:

> Liou, N. S. Y., De, T., Urbanski, A., Chieng, C., Kong, Q., David, A. L., Khasriya, R., Yakimovich, A., & Horsley, H.
> A clinical microscopy dataset to develop a deep learning diagnostic test for urinary tract infection.
> Scientific Data, 11, 155 (2024). [https://doi.org/10.1038/s41597-024-02975-0](https://doi.org/10.1038/s41597-024-02975-0) 

The dataset contains 300 microscopy images, with 3,562 annotated urinary cells. Each image has an associated segmentation mask where pixels are labeled into 7 clinically relevant cell classes.

## Dataset Structure

After download, the dataset is organized into three root folders, each having three folders with images:

```bash
data/
├── train/
│   ├── img/         # Raw microscopy images (TIFF, 1392×1040)
│   ├── bin_mask/    # Binary masks (0 = background, 1 = foreground)
│   └── mult_mask/   # Multiclass masks (0 = background, 1–7 = urinary cell types)
├── test/
└── validation/
```

## Download Instructions 

The dataset is **not included in this repository**. You can obtain it from the official source:

- Rodare repository (DOI: [10.14278/rodare.2562](https://doi.org/10.14278/rodare.2562))

## Using the Dataset in Google Colab

Since this project was developed in **Google Colab** , the dataset was mounted from **Google Drive**.

Example setup in Colab:

```python
from google.colab import drive
drive.mount('/content/drive')

# Navigate to dataset location
!ls /content/drive/MyDrive/clinical_microscopy_dataset/

# (Optional) copy into working directory
!cp -r /content/drive/MyDrive/clinical_microscopy_dataset ./data
```

## Preprocessing

Following the original paper, images were:
- **Resized** into 256 × 256 pixels for training,
- **Normalized** to values in [-1, 1],

For this thesis, only the **multiclass masks** were used in training.

## License & Usage

- The dataset is released under the **MIT License** by the authors.
- Please **cite the dataset paper** if you use it in academic work (see citation above).
