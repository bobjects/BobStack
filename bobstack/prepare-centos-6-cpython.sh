#!/bin/bash
set -e
# Any subsequent(*) commands which fail will cause the shell script to exit immediately

PYTHONVERSION=2.7.11
SETUPTOOLSVERSION=1.4.2

cd ~
if [ ! -d src ]
then
	mkdir src
fi
cd src

# Notes for installing pypy:
# sudo yum install ncurses-devel libffi-devel expat-devel
# sudo rpm -Uvh http://pkgs.repoforge.org/mercurial/mercurial-2.2.2-1.el6.rfx.x86_64.rpm
# hg clone http://bitbucket.org/pypy/pypy pypy
# cd pypy/pypy/goal
# python ../../rpython/bin/rpython --opt=jit

sudo yum -y update
sudo wget http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el6.rf.x86_64.rpm
sudo rpm -Uhv rpmforge-release*.rf.x86_64.rpm
sudo yum groupinstall -y development
sudo yum install -y zlib-dev openssl-devel sqlite-devel bzip2-devel xz-libs wget man htop
wget -c http://www.python.org/ftp/python/$PYTHONVERSION/Python-$PYTHONVERSION.tar.xz
xz -dk Python-$PYTHONVERSION.tar.xz
tar -xvf Python-$PYTHONVERSION.tar
rm Python-$PYTHONVERSION.tar
cd Python-$PYTHONVERSION
./configure --prefix=/usr/local    
# If we wanted to not set the new version as the system default, we would use "altinstall" instead of "install"
make
sudo make install


# only need to run this if python version is less than 2.7.9.
cd ~/src
wget -c --no-check-certificate https://pypi.python.org/packages/source/s/setuptools/setuptools-$SETUPTOOLSVERSION.tar.gz
tar -xvf setuptools-$SETUPTOOLSVERSION.tar.gz
cd setuptools-$SETUPTOOLSVERSION
sudo python setup.py install
curl https://bootstrap.pypa.io/get-pip.py | sudo python -

sudo pip install virtualenv

