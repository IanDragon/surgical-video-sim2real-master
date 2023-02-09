### Long-Term Temporally Consistent Unpaired Video Translation from Simulated Surgical 3D Data

This is the official implementation of our ICCV '21 [paper](https://arxiv.org/abs/2103.17204) for unpaired synthesis of view-consistent surgical video sequences.

![example image](example.png)

Since our model was trained on non-public patient data, this repository contains only a dummy dataset in order to provide a minimal, executable code base. However, the data that our model generated can be directly downloaded from our [project page](http://opencas.dkfz.de/video-sim2real/).

### Data Generation

Training data:
```
cd simulated_data_generation
blender ExampleScene_FakeLiver.blend -b -P renderRandomImages.py -- --images 10 --test_render --texture_patch_size 512
```

Synthetic reference images and render data (texture-pixel correspondences, interpolation weights) for domain A will be written to ```data/simulated/```.

Test data:
```
cd simulated_data_generation
blender ExampleScene_FakeLiver.blend -b -P renderSequences.py -- --test_render --texture_patch_size 512
```

This will be written to ```data/simulated_sequences/```. Note that the ```train.py``` script translates and saves test images every N iterations. So test data has to be generated before training.

### Training

After synthetic data was generated, run the following to train the model:
```
cd translation_model
python3 train.py --output_path trials/test_trial
```

### Dependences

The code was tested on:
> Python 3.8.5, Pytorch 1.5.0, Blender 2.79b, Torchvision 0.6.0

### Citation

This work was presented at the [IEEE/CVF International Conference on Computer Vision 2021](https://iccv2021.thecvf.com/home). If you use this code, please cite our paper:

```
@InProceedings{Rivoir_2021_ICCV,
    author    = {Rivoir, Dominik and Pfeiffer, Micha and Docea, Reuben and Kolbinger, Fiona and Riediger, Carina and Weitz, J\"urgen and Speidel, Stefanie},
    title     = {Long-Term Temporally Consistent Unpaired Video Translation From Simulated Surgical 3D Data},
    booktitle = {Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)},
    month     = {October},
    year      = {2021},
    pages     = {3343-3353}
}
```

This work was carried out at the National Center for Tumor Diseases (NCT) Dresden, [Department of Translational Surgical Oncology](https://www.nct-dresden.de/tso.html) and the Centre for Tactile Internet ([CeTI](https://ceti.one/)) at TU Dresden.

### License

Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode). 

Note that this is a direct modification of Pfeiffer et al.'s ([Paper](https://arxiv.org/abs/1907.02882), [GitLab](https://gitlab.com/nct_tso_public/laparoscopic-image-2-image-translation/)) work and the MUNIT framework ([Paper](https://arxiv.org/abs/1804.04732), [GitHub](https://github.com/NVlabs/MUNIT)). The original Copyright holder is NVIDIA Corporation:

Copyright (C) 2018 NVIDIA Corporation.  All rights reserved.
Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode). 

Additionally, we use the MS-SSIM implementation (```translation_model/pytorch_msssim``` folder) by Jorge Pessoa ([GitHub](https://github.com/jorge-pessoa/pytorch-msssim)) which is licensed under the MIT license.

These licenses allow you to use, modify and share the project for non-commercial use as long as you adhere to the conditions of the license above.

### Contact

If you have any questions, do not hesitate to contact us: ```dominik.rivoir [at] nct-dresden.de```