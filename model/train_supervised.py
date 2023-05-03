import os
from fasttext import train_supervised

if __name__ == "__main__":
    train_data = os.path.join(os.getenv("DATADIR", ''), 'train.txt')

    model = train_supervised(
        input=train_data, epoch=25, lr=1.0, wordNgrams=2
    )
    model.save_model("action.bin")