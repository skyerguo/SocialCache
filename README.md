# SocNet

# 基本环境配置

## 导入github的仓库

```
sudo apt-get update && sudo apt-get -yqq install git
cd ~/.ssh && ssh-keygen -C gtc -f id_rsa -t rsa -N ''
cat id_rsa.pub
```

将公钥复制到 `https://github.com/settings/ssh/new`

```
git config --global user.name skyerguo97 && git config --global user.email skyerguo97@gmail.com
cd ~ && git clone git@github.com:skyerguo/SocNet.git
```

## 安装zsh

sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
sudo usermod -s /bin/zsh gtc

## 安装必要的库

```
cd ~/SocNet && sh environment_initialize.sh
```

## 重启生效

```
sudo reboot

sudo sysctl -w kernel.threads-max=2061206
sudo sysctl -w kernel.pid_max=4194303
sudo sysctl -w vm.max_map_count=4194303
sudo /usr/local/etc/emulab/rc/rc.mounts boot
```

