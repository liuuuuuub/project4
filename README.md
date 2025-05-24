# project4



git clone https://github.com/sxyu/svox2.git
cd svox2
conda env create -f environment.yml
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121
conda install -c nvidia cuda-toolkit=12.1

python setup.py install
