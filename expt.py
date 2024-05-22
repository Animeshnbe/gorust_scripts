import torch
import tqdm
from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering, pipeline, AdamW
from torch.utils.data import DataLoader, Dataset, TensorDataset, random_split
from datasets import load_dataset

dataset = load_dataset("keivalya/MedQuad-MedicalQnADataset")
dataset = dataset["train"]

tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

tokenized_datasets = {
    'train': tokenizer([(example['Question'], example['Answer']) for example in train_dataset], truncation=True, padding=True),
    'val': tokenizer([(example['Question'], example['Answer']) for example in val_dataset], truncation=True, padding=True),
}

train_dataloader = DataLoader(
    TensorDataset(*[torch.tensor(tokenized_datasets['train'][key], dtype=torch.long) for key in tokenized_datasets['train']]),
    batch_size=2,
    shuffle=True
)

val_dataloader = DataLoader(
    TensorDataset(*[torch.tensor(tokenized_datasets['val'][key], dtype=torch.long) for key in tokenized_datasets['val']]),
    batch_size=2,
    shuffle=False
)

model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-cased')

optimizer = AdamW(model.parameters(), lr=5e-4)

# Training loop
num_epochs = 3
device = "cuda:0"

for epoch in range(num_epochs):
    model.train()
    train_loss = 0.0
    for batch in tqdm(train_dataloader, desc=f'Epoch {epoch + 1}/{num_epochs}', leave=False):
        inputs = {
            'input_ids': batch[0].to(device),
            'attention_mask': batch[1].to(device),
            'start_positions': batch[0].to(device),
            'end_positions': batch[0].to(device)
        }
        outputs = model(**inputs)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        train_loss += loss.item()

    # Validation loop
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for batch in tqdm(val_dataloader, desc='Validation', leave=False):
            inputs = {
                'input_ids': batch[0].to(device),
                'attention_mask': batch[1].to(device),
                'start_positions': batch[0].to(device),
                'end_positions': batch[0].to(device)
            }
            outputs = model(**inputs)
            loss = outputs.loss
            val_loss += loss.item()

    avg_train_loss = train_loss / len(train_dataloader)
    avg_val_loss = val_loss / len(val_dataloader)

    print(f'Epoch {epoch + 1}/{num_epochs} - Avg Training Loss: {avg_train_loss:.4f} - Avg Validation Loss: {avg_val_loss:.4f}')