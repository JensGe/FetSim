# owi Fetcher Simulator

## Settings

**/home/ubuntu/init_docker.sh**
```shell script
sudo docker pull dockerjens23/fetsim
sudo sleep 2s
sudo docker run -d -p 80:80 dockerjens23/fetsim
```

**crontab -e**
```
@reboot sudo /home/ubuntu/init_docker.sh
```

