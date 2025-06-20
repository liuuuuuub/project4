
Install environment:
```
conda create -n TensoRF python=3.8
conda activate TensoRF
pip install torch torchvision
pip install tqdm scikit-image opencv-python configargparse lpips imageio-ffmpeg kornia lpips tensorboard
```

## Quick Start
The training script is in `train.py`, to train a TensoRF:

```
python train.py --config configs/lego.txt
```

## Rendering

```
python train.py --config configs/lego.txt --ckpt path/to/your/checkpoint --render_only 1 --render_test 1 
```

## Extracting mesh
You can also export the mesh by passing `--export_mesh 1`:
```
python train.py --config configs/lego.txt --ckpt path/to/your/checkpoint --export_mesh 1
```


![Uploading 059999_001.png…]()

