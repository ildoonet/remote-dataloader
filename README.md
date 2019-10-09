# remote-dataloader
DataLoader processed in multiple remote computation machines for heavy data processing

## Example.py

```
$ python example.py     # run server(dataloader)
$ python remote_dataloader/worker.py --server 0.0.0.0:1958      # run workers
$ python remote_dataloader/worker.py --server 0.0.0.0:1958  
```
