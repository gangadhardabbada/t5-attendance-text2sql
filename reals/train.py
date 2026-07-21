import os
import json
import torch
import evaluate
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq,
    EarlyStoppingCallback
)

def main():
    os.makedirs('C:/games/t5/reals/model', exist_ok=True)
    os.makedirs('C:/games/t5/reals/tokenizer', exist_ok=True)

    # 1. Load Datasets
    data_files = {
        "train": "C:/games/t5/reals/train_dataset.csv",
        "validation": "C:/games/t5/reals/validation_dataset.csv"
    }
    dataset = load_dataset("csv", data_files=data_files)

    # 2. Tokenizer and Model
    model_name = "t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # 3. Preprocessing
    max_source_length = 256
    max_target_length = 256

    def preprocess_function(examples):
        inputs = examples["input_text"]
        targets = examples["target_text"]
        
        # Tokenize inputs
        model_inputs = tokenizer(inputs, max_length=max_source_length, truncation=True, padding="max_length")
        
        # Tokenize targets
        labels = tokenizer(targets, max_length=max_target_length, truncation=True, padding="max_length")
        
        # Replace padding token id with -100 to ignore in loss
        labels["input_ids"] = [
            [(l if l != tokenizer.pad_token_id else -100) for l in label] for label in labels["input_ids"]
        ]
        
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    tokenized_datasets = dataset.map(preprocess_function, batched=True, remove_columns=dataset["train"].column_names)

    # 4. Training Arguments
    fp16_available = torch.cuda.is_available()
    
    args = Seq2SeqTrainingArguments(
        output_dir="C:/games/t5/reals/model_checkpoints",
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=3e-4,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        gradient_accumulation_steps=2,
        weight_decay=0.01,
        save_total_limit=2,
        num_train_epochs=10,
        predict_with_generate=True,
        fp16=fp16_available,
        warmup_steps=100,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        report_to="none"
    )

    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    # 5. Trainer
    trainer = Seq2SeqTrainer(
        model=model,
        args=args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"],
        data_collator=data_collator,
        processing_class=tokenizer,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
    )

    # 6. Train
    train_result = trainer.train()
    
    # 7. Save Model and Metrics
    trainer.save_model("C:/games/t5/reals/model")
    tokenizer.save_pretrained("C:/games/t5/reals/tokenizer")
    
    metrics = train_result.metrics
    trainer.log_metrics("train", metrics)
    trainer.save_metrics("train", metrics)
    trainer.save_state()
    
    with open("C:/games/t5/reals/training_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    with open('C:/games/t5/reals/execution.log', 'a', encoding='utf-8') as f:
        f.write("\\nPHASE 7 - TRAINING COMPLETED\\n")
        f.write(f"Metrics: {metrics}\\n")

    print("Training finished successfully.")

if __name__ == "__main__":
    main()
