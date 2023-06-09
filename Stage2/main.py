import os
import sys
sys.path.append(os.getcwd())
import json
import pandas as pd
from img_pipeline import ImagePipelines


if __name__ == '__main__':
    dataset = pd.read_csv('data/MAMI/trial.csv', delimiter='\t')
    dataset = dataset[:3]
    image_models = ImagePipelines()
    for _, row in dataset.iterrows():
        mami_results = {
            'file': row[0],
            'task_label': [dataset.columns[i] for i in range(1, 6) if row[i] == 1],
            'text transcription': row[-1],
        }

        img_path = os.path.join('data/MAMI/images', row[0])
        for task_label in image_models.tasks:
            print(f'Processing {task_label}')
            result = image_models.get_results(img_path, task_label)
            mami_results[task_label] = result

        with open('mami_results.jsonl', 'a') as f:
            json.dump(mami_results, f)
            f.write('\n')
