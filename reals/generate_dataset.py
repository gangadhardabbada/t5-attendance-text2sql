import os
import psycopg2
import csv
import random
import datetime
from collections import Counter
from dotenv import load_dotenv

load_dotenv('C:/games/t5/.env', override=True)
db_url = os.getenv('DATABASE_URL')

def get_connection():
    return psycopg2.connect(db_url, sslmode='require')

# Load real data from slm/final_dataset.csv
NAMES = set()
SUBJECTS = set()
dates_set = set()

with open('C:/games/t5/slm/final_dataset.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('student_name'): NAMES.add(row['student_name'])
        if row.get('subject_name'): SUBJECTS.add(row['subject_name'])
        if row.get('date'): dates_set.add(row['date'])

NAMES = list(NAMES)[:100]  # Limit to 100 for generation combinations
SUBJECTS = list(SUBJECTS)[:30]
dates = list(dates_set)[:50]
STATUSES = ['Present', 'Absent']

def generate_queries():
    dataset = []
    
    # Synonyms for diversity
    show_syns = ["Show", "Display", "List", "Get", "Provide", "Find", "What is", "I need", "Can you show me"]
    att_syns = ["attendance", "attendance records", "presence or absence", "records"]
    student_syns = ["students", "pupils", "enrolled members", "people"]
    
    # Dates are loaded from real data
    # (Removed synthetic date generation)
    
    # 1. Student Queries (Target: ~2000)
    for name in NAMES:
        for _ in range(250):
            d = random.choice(dates)
            s_show = random.choice(show_syns)
            dataset.append({
                "template": "student_enrollment",
                "category": "Student",
                "question": f"{s_show} when {name} enrolled.",
                "query": f"SELECT enrollment_date FROM students_master WHERE name = '{name}';"
            })
            dataset.append({
                "template": "student_id",
                "category": "Student",
                "question": f"{s_show} the ID of {name}.",
                "query": f"SELECT student_id FROM students_master WHERE name = '{name}';"
            })
            dataset.append({
                "template": "student_after_date",
                "category": "Student",
                "question": f"{s_show} {random.choice(student_syns)} who enrolled after {d}.",
                "query": f"SELECT name FROM students_master WHERE enrollment_date > '{d}';"
            })
            
    # 2. Attendance Queries (Target: ~2000)
    for name in NAMES:
        for sub in SUBJECTS:
            for stat in STATUSES:
                for _ in range(15):
                    s_show = random.choice(show_syns)
                    s_att = random.choice(att_syns)
                    dataset.append({
                        "template": "attendance_status",
                        "category": "Attendance",
                        "question": f"{s_show} dates when {name} was {stat} in {sub}.",
                        "query": f"SELECT a.attendance_date FROM consolidated_attendance_records a JOIN students_master st ON a.student_id = st.student_id JOIN subjects_master su ON a.subject_id = su.subject_id WHERE st.name = '{name}' AND su.subject_name = '{sub}' AND a.status = '{stat}';"
                    })
                    dataset.append({
                        "template": "attendance_count",
                        "category": "Attendance",
                        "question": f"How many times was {name} marked {stat} for {sub}?",
                        "query": f"SELECT COUNT(*) FROM consolidated_attendance_records a JOIN students_master st ON a.student_id = st.student_id JOIN subjects_master su ON a.subject_id = su.subject_id WHERE st.name = '{name}' AND su.subject_name = '{sub}' AND a.status = '{stat}';"
                    })

    # 3. Subject Queries (Target: 1000)
    for sub in SUBJECTS:
        for _ in range(100):
            s_show = random.choice(show_syns)
            dataset.append({
                "template": "subject_records",
                "category": "Subject",
                "question": f"{s_show} all records for the {sub} subject.",
                "query": f"SELECT * FROM consolidated_attendance_records a JOIN subjects_master su ON a.subject_id = su.subject_id WHERE su.subject_name = '{sub}';"
            })
            dataset.append({
                "template": "subject_id",
                "category": "Subject",
                "question": f"{s_show} the subject ID for {sub}.",
                "query": f"SELECT subject_id FROM subjects_master WHERE subject_name = '{sub}';"
            })

    # 4. Faculty / Logs Queries (Target: 1000)
    for d in dates:
        for _ in range(3):
            s_show = random.choice(show_syns)
            dataset.append({
                "template": "faculty_logs",
                "category": "Faculty",
                "question": f"{s_show} the administrative logs on {d}.",
                "query": f"SELECT * FROM transaction_logs WHERE log_date::date = '{d}';"
            })

    # 5. Aggregate stats (Target: 1000)
    for _ in range(500):
        s_show = random.choice(show_syns)
        dataset.append({
            "template": "agg_students",
            "category": "Aggregate statistics",
            "question": f"{s_show} the total number of students.",
            "query": "SELECT COUNT(*) FROM students_master;"
        })
        dataset.append({
            "template": "agg_subjects",
            "category": "Aggregate statistics",
            "question": f"{s_show} the total number of subjects offered.",
            "query": "SELECT COUNT(*) FROM subjects_master;"
        })
        
    # 6. Admin Reports (Target: 500)
    for _ in range(500):
        dataset.append({
            "template": "admin_report",
            "category": "Administrative reports",
            "question": f"{random.choice(show_syns)} a full joined report of all attendance.",
            "query": "SELECT st.name, su.subject_name, a.attendance_date, a.status FROM consolidated_attendance_records a JOIN students_master st ON a.student_id = st.student_id JOIN subjects_master su ON a.subject_id = su.subject_id;"
        })

    # 7. Complex Multi-table
    for name in NAMES:
        for _ in range(100):
            dataset.append({
                "template": "complex_distinct",
                "category": "Complex multi-table analytical queries",
                "question": f"{random.choice(show_syns)} the unique subjects that {name} attended.",
                "query": f"SELECT DISTINCT su.subject_name FROM consolidated_attendance_records a JOIN students_master st ON a.student_id = st.student_id JOIN subjects_master su ON a.subject_id = su.subject_id WHERE st.name = '{name}';"
            })

    # Deduplicate strictly by question text to ensure diversity
    unique = {}
    for item in dataset:
        if item['question'] not in unique:
            unique[item['question']] = item
            
    final_list = list(unique.values())
    random.shuffle(final_list)
    return final_list[:8000]

def main():
    try:
        conn = get_connection()
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    raw_dataset = generate_queries()
    print(f"Generated {len(raw_dataset)} unique queries for validation.")
    
    # We will only EXPLAIN a representative sample per template
    # as requested by the user, to speed up validation.
    templates_validated = set()
    validated_dataset = []
    rejected = 0
    operators_count = Counter()
    category_count = Counter()
    
    with conn.cursor() as cur:
        for item in raw_dataset:
            template = item.get("template")
            q = item["query"]
            
            # If we haven't validated this template yet, do EXPLAIN
            if template not in templates_validated:
                try:
                    cur.execute(f"EXPLAIN {q}")
                    templates_validated.add(template)
                except Exception as e:
                    conn.rollback()
                    rejected += 1
                    continue # Skip adding this and we won't mark template as validated
                    
            # If we reach here, it belongs to a validated template pattern
            validated_dataset.append(item)
            category_count[item['category']] += 1
            
            uq = q.upper()
            if " JOIN " in uq: operators_count["JOIN"] += 1
            if " WHERE " in uq: operators_count["WHERE"] += 1
            if " GROUP BY " in uq: operators_count["GROUP BY"] += 1
            if " COUNT(" in uq: operators_count["COUNT"] += 1
            if " DISTINCT " in uq: operators_count["DISTINCT"] += 1
                
    conn.close()
    
    print(f"Validation complete. Valid: {len(validated_dataset)}, Rejected: {rejected}")
    
    X = [{"question": row["question"], "query": row["query"]} for row in validated_dataset]
    total = len(X)
    train_end = int(total * 0.8)
    val_end = int(total * 0.9)
    
    X_train = X[:train_end]
    X_val = X[train_end:val_end]
    X_test = X[val_end:]
    
    def write_csv(path, data):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['question', 'query'])
            writer.writeheader()
            writer.writerows(data)
            
    write_csv('C:/games/t5/reals/full_dataset.csv', X)
    write_csv('C:/games/t5/reals/train_dataset.csv', X_train)
    write_csv('C:/games/t5/reals/validation_dataset.csv', X_val)
    write_csv('C:/games/t5/reals/test_dataset.csv', X_test)
    
    q_len_avg = sum(len(x['question']) for x in X) / len(X)
    sql_len_avg = sum(len(x['query']) for x in X) / len(X)
    cat_str = "\\n".join(f"- {k}: {v}" for k, v in category_count.items())
    op_str = "\\n".join(f"- {k}: {v}" for k, v in operators_count.items())
    
    stats_md = f"""# Dataset Statistics

## Totals
- **Total valid examples**: {len(X)}
- **Rejected examples**: {rejected}
- **Duplicates removed**: Handled via dict hashing on generation

## Category Distribution
{cat_str}

## SQL Operator Frequency
{op_str}

## Averages
- **Average question length**: {q_len_avg:.2f} characters
- **Average SQL length**: {sql_len_avg:.2f} characters

## Splits
- **Training**: {len(X_train)}
- **Validation**: {len(X_val)}
- **Testing**: {len(X_test)}
"""
    with open('C:/games/t5/reals/dataset_statistics.md', 'w', encoding='utf-8') as f:
        f.write(stats_md)
        
    with open('C:/games/t5/reals/execution.log', 'a', encoding='utf-8') as f:
        f.write(f"\nPHASE 5 & 6 — DATASET EXPANSION AND SPLIT\n")
        f.write(f"Generated and validated {len(X)} queries using EXPLAIN sampling.\n")
        f.write(f"Splits: Train={len(X_train)}, Val={len(X_val)}, Test={len(X_test)}\n")
        f.write(f"Statistics generated in dataset_statistics.md.\n")

    print("Phases 5 and 6 complete.")

if __name__ == "__main__":
    main()
