### Requirements
- running server of `rabbitmq`
- running server of `Lumen`
- 'Nginx' proxy port for listening 
---
### Running services
```
bash
sudo vim /lib/systemd/system/havijMQ.service
sudo systemctl daemon-reload
sudo systemctl enable havijMQ.service
sudo systemctl start havijMQ.service
sudo systemctl restart havijMQ.service
sudo systemctl status havijMQ.service
sudo journalctl -f --no-pager -n 1000 --output=cat -u havijMQ
```