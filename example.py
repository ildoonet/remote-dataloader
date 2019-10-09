import torchvision as torchvision
from torchvision.transforms import transforms
from tqdm import tqdm

from remote_dataloader.loader import RemoteDataLoader

if __name__ == '__main__':
    transform_train = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])

    total_trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform_train)
    loader = RemoteDataLoader(total_trainset, batch_size=32, timeout=5)

    for epoch in range(5):
        for img, lb in tqdm(loader):
            pass
