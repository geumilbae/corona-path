#!/bin/sh
num_param=$#
if [ num_param<1 ]; then
    echo "크롬 버전을 입력하세요. $ download_chromedriver.sh {크롬 버전}"
fi
version=$1

fn_driver_linux=chromedriver_linux64.zip
fn_driver_mac=chromedriver_mac64.zip
fn_driver_win=chromedriver_win32.zip

wget -P . https://chromedriver.storage.googleapis.com/$1/$fn_driver_linux
wget -P . https://chromedriver.storage.googleapis.com/$1/$fn_driver_mac
wget -P . https://chromedriver.storage.googleapis.com/$1/$fn_driver_win
wget -P . https://chromedriver.storage.googleapis.com/$1/notes.txt

unzip ./$fn_driver_linux
mv ./chromedriver ./chromedriver_linux
unzip ./$fn_driver_mac
mv ./chromedriver ./chromedriver_mac
unzip ./$fn_driver_win
mv ./chromedriver.exe ./chromedriver_win.exe

rm ./$fn_driver_linux
rm ./$fn_driver_mac
rm ./$fn_driver_win