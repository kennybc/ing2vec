import os
import evaluate
import numpy as np
from pathlib import Path
from torch.utils.data import random_split
from parser.preprocess import label2id, model, tokenizer
from parser.preprocess import preprocess_data, tokenize_labels
from transformers import (
    logging,
    DataCollatorForTokenClassification,
    TrainingArguments,
    Trainer,
)

here = Path(__file__).parent


# keep terminal clear of warnings/low-level messages
logging.set_verbosity_error()
os.environ["TOKENIZERS_PARALLELISM"] = "false"


# split a given dataset into a training set and a testing set
def split_data(data, train_size=0.9):
    train_size = int(train_size * len(data))
    test_size = len(data) - train_size
    return random_split(data, [train_size, test_size])


# fine-tune a pre-trained model using tsv data from a given file path
def train(data_path=here / "./data/train_full.tsv", save_path=here / "./model"):
    data = preprocess_data(data_path)
    tokenized_data = tokenize_labels(data)
    train_data, test_data = split_data(tokenized_data)

    data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)
    seqeval = evaluate.load("seqeval")
    label_list = list(label2id.keys())

    # compute the precision, recall, f1 score, and accuracy of a given prediction
    def compute_metrics(p):
        predictions, labels = p
        predictions = np.argmax(predictions, axis=2)

        true_predictions = [
            [label_list[p] for (p, l) in zip(prediction, label) if l != -100]
            for prediction, label in zip(predictions, labels)
        ]
        true_labels = [
            [label_list[l] for (p, l) in zip(prediction, label) if l != -100]
            for prediction, label in zip(predictions, labels)
        ]

        results = seqeval.compute(predictions=true_predictions, references=true_labels)
        return {
            "precision": results["overall_precision"],
            "recall": results["overall_recall"],
            "f1": results["overall_f1"],
            "accuracy": results["overall_accuracy"],
        }

    training_args = TrainingArguments(
        output_dir=save_path,
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=4,
        weight_decay=0.01,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        resume_from_checkpoint=True,
        push_to_hub=False,
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_data,
        eval_dataset=test_data,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )
    trainer.train()
    trainer.save_model()
