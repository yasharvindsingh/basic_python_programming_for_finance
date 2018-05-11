#! /bin/bash
sudo apt-get install python-pip
sudo apt-get install python3-pip
sudo pip3 install numpy pandas matplotlib quandl six scipy scikit-learn seaborn keras tensorflow keras-rl beautifulsoup4 pandas_datareader xlrd 
git clone --recursive "https://github.com/matplotlib/mpl_finance.git"
cd mpl_finance
sudo python setup.py install
sudo pyhton3 setup.py install


