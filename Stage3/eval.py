import os
import json
from evaluate import load


def eval(json_list, file, acc, bleu, rouge, meteor):
    label_preds = []
    label_gold = []
    rationale_preds = []
    rationale_gold = []

    for json_str in json_list:
        res = json.loads(json_str)
        label_preds.append(res["answer"])
        label_gold.append(res["gold_answer"])
        rationale_preds.append(res["rationale"])
        rationale_gold.append(res["gold_rationale"])

    acc_res = acc.compute(predictions=label_preds, references=label_gold)
    bleu_res = bleu.compute(predictions=rationale_preds, references=rationale_gold)
    rouge_res = rouge.compute(predictions=rationale_preds, references=rationale_gold)
    meteor_res = meteor.compute(predictions=rationale_preds, references=rationale_gold)

    return {
        'file': file,
        'accuracy': acc_res['exact_match'],
        'bleu': bleu_res['bleu'],
        'rouge': rouge_res['rougeL'],
        'meteor': meteor_res['meteor']
    }


if __name__ == "__main__":
    acc = load('exact_match')
    bleu = load('bleu')
    rouge = load('rouge')
    meteor = load('meteor')

    for file in sorted(os.listdir('Stage3/inference/')):
        print(f'-----Evalutating {file}-----')
        if file.endswith('.jsonl'):
            path = os.path.join('Stage3/inference/', file)
            with open(path, 'r') as json_file:
                json_list = list(json_file)

            results = eval(json_list, file, acc, bleu, rouge, meteor)

            with open('Stage3/results.jsonl', 'a') as f:
                json.dump(results, f)
                f.write('\n')
