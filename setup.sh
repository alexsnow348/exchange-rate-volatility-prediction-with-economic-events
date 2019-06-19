# Install Python
apt-get install python3-dev python3-pip  -y

# Install Miniconda
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda-latest-Linux-x86_64.sh
bash Miniconda-latest-Linux-x86_64.sh
rm -f Miniconda3-latest-Linux-x86_64.sh

# Create virtual envs for Volatility Prediction with Eco Event
conda create -n VE python=3.6 -y
conda activate VE
pip install -r  requirements.txt
