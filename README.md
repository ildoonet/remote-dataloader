# remote-dataloader
DataLoader processed in multiple remote computation machines for heavy data processing

## Example.py

```bash
$ python example.py     # run server(dataloader)
$ python remote_dataloader/worker.py --server {master_ip}:1958      # run multiple workers
$ python remote_dataloader/worker.py --server {master_ip}:1958
$ ...  
```
