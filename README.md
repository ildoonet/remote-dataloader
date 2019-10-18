# remote-dataloader

DataLoader processed in multiple remote computation machines for heavy data processing. 

## Architecture

## Usage

### RemoteDataLoader

```python
total_trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform_train)
loader = RemoteDataLoader(total_trainset, batch_size=32, timeout=5)
````

### Example.py

```example.py``` contains a simple example to process cifar10 images using remote nodes.

```bash
$ python example.py     # run server(dataloader)
$ python remote_dataloader/worker.py --server {master_ip}:1958      # run multiple workers
$ python remote_dataloader/worker.py --server {master_ip}:1958
$ ...  
```
