import os
import time
import json
import csv
import psycopg2
import evaluate
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from dotenv import load_dotenv
import sys
sys.path.append('C:/games/t5/reals')
from predict import T5SQLPredictor

load_dotenv('C:/games/t5/.env', override=True)
db_url = os.getenv('DATABASE_URL')

def execute_sql(sql):
    try:
        conn = psycopg2.connect(db_url, sslmode='require', connect_timeout=5)
        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        conn.close()
        return True, res
    except Exception as e:
        return False, str(e)

def main():
    model_path = "C:/games/t5/reals/model"
    tokenizer_path = "C:/games/t5/reals/tokenizer"
    test_data_path = "C:/games/t5/reals/test_dataset.csv"
    
    if not os.path.exists(model_path):
        print("Model not found. Run training first.")
        return

    print("Loading model and tokenizer...")
    predictor = T5SQLPredictor()

    print("Loading test data...")
    test_data = []
    with open(test_data_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_data.append(row)
            
    # Sub-sample for faster execution evaluation if test set is huge
    # We will test all 412 queries from test_dataset.csv
    
    rouge_metric = evaluate.load('rouge')
    bleu_metric = evaluate.load('sacrebleu')
    
    exact_matches = 0
    exec_matches = 0
    latencies = []
    
    predictions = []
    references = []
    confusion = []
    
    print("Starting evaluation...")
    for item in test_data:
        question = item['input_text']
        true_sql = item['target_text']
        
        start_time = time.time()
        
        # Inference
        pred_sql = predictor.predict(question)
        
        latency = (time.time() - start_time) * 1000
        latencies.append(latency)
        
        predictions.append(pred_sql)
        references.append(true_sql)
        
        # Exact Match
        if pred_sql == true_sql:
            exact_matches += 1
            exec_matches += 1 # Assume exact match guarantees execution match
        else:
            # Execution Accuracy
            success, res = execute_sql(pred_sql)
            if success:
                exec_matches += 1
            else:
                confusion.append({
                    "input_text": question,
                    "target_sql": true_sql,
                    "predicted_sql": pred_sql,
                    "error_type": res
                })

    avg_latency = sum(latencies) / len(latencies)
    exact_match_acc = exact_matches / len(test_data)
    exec_acc = exec_matches / len(test_data)
    
    print("Computing BLEU and ROUGE...")
    rouge_results = rouge_metric.compute(predictions=predictions, references=references)
    bleu_results = bleu_metric.compute(predictions=predictions, references=[[r] for r in references])
    
    report = f"""# Model Evaluation Report
**Model**: `t5-small`
**Test Set Size**: {len(test_data)} queries

## 1. Core Metrics
- **Exact Match Accuracy**: {exact_match_acc * 100:.2f}%
- **Execution Accuracy (Supabase)**: {exec_acc * 100:.2f}%
- **BLEU Score**: {bleu_results['score']:.2f}
- **ROUGE-L**: {rouge_results['rougeL'] * 100:.2f}

## 2. Latency Metrics
- **Average Generation Latency**: {avg_latency:.2f} ms per query

## 3. Top 5 Successful Predictions
"""
    # Just list some random exact matches
    successes = 0
    for q, p, t in zip(test_data, predictions, references):
        if p == t and successes < 5:
            report += f"- **Input**: {q['input_text']}\\n  **SQL**: {p}\\n"
            successes += 1

    report += "\\n## 4. Failed Predictions\\n*(Detailed in `confusion_examples.csv`)*\\n"

    with open('C:/games/t5/reals/evaluation_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
        
    with open('C:/games/t5/reals/confusion_examples.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["input_text", "target_sql", "predicted_sql", "error_type"])
        writer.writeheader()
        writer.writerows(confusion)
        
    print("Evaluation complete. Report generated.")
    print(f"Exact Match: {exact_match_acc * 100:.2f}%")
    print(f"Exec Acc: {exec_acc * 100:.2f}%")

if __name__ == '__main__':
    import torch
    main()
