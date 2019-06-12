echo Get Server Program
wget  https://github.com/SoftEtherVPN/SoftEtherVPN_Stable/releases/download/v4.29-9680-rtm/softether-vpnserver-v4.29-9680-rtm-2019.02.28-linux-x64-64bit.tar.gz
tar xzvf softether-vpnserver-v4.29-9680-rtm-2019.02.28-linux-x64-64bit.tar.gz

echo Init Make
apt-get update
apt-get install git-core gnupg flex bison gperf build-essential
cd vpnserver
./.install.sh
