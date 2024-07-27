import os
import json
import random
from collections import defaultdict, deque
from data_manager import DataManager
from tqdm import tqdm
import argparse
from prompt_templates import ONTOLOGY_REASON_PROMPT, CLOSE_PATH_REASON_PROMPT, OPEN_PATH_REASON_PROMPT, EXPLAINING_PROMPT
from llm_api import run_llm_chat

def bfs_paths(entity2relationtail_dict, start, goal, max_hops, max_paths):
    queue = deque([(start, [], 0, set([start]))])
    paths = []
    while queue:
        current, path, hops, visited = queue.popleft()
        if hops < max_hops:
            for relation, neighbor, direction in entity2relationtail_dict[current]:
                if direction == 1:
                    new_path = path + [(current, relation, neighbor)]
                else:
                    new_path = path + [(neighbor, relation, current)]
                if neighbor == goal:
                    paths.append(new_path)
                elif neighbor not in visited:
                    queue.append((neighbor, new_path, hops + 1, visited | set([neighbor])))
    return paths[:max_paths]

def close_path_finder(data_manager: DataManager, head, tail):
    close_paths = list(bfs_paths(data_manager.entity2relationtail_dict, head, tail, data_manager.max_path_hops, data_manager.max_paths))
    if close_paths:
        path_degrees = []
        for path in close_paths:
            degree_sum = sum(data_manager.relation_degree_dict[relation] for _, relation, _ in path)
            path_degrees.append((degree_sum, path))
        path_degrees.sort(key=lambda x: x[0])

        top_paths = [path for _, path in path_degrees[:data_manager.max_paths]]
        top_paths.reverse()
        return top_paths
    return []

def build_instructions(dataset, train_size):
    setting = "transductive" # 指令构建默认是transductive，用训练集
    
    data_manager = DataManager(dataset=dataset, setting=setting, train_size=train_size)

    paths_dir = f"instructions/{dataset}"
    os.makedirs(paths_dir, exist_ok=True)

    sft_instructions = []
    
    for pos_triple in tqdm(data_manager.path_set, desc=f"Processing {dataset} - setting: {setting} - Train_size: {train_size}"):
        pos_head, relation, pos_tail = pos_triple
        removed_from_head = (relation, pos_tail, 1)
        removed_from_tail = (relation, pos_head, -1)
        
        # 移除当前triple，因为是寻找当前(pos_head, pos_tail)的close_path
        if removed_from_head in data_manager.entity2relationtail_dict[pos_head]:
            data_manager.entity2relationtail_dict[pos_head].remove(removed_from_head)
        if removed_from_tail in data_manager.entity2relationtail_dict[pos_tail]:
            data_manager.entity2relationtail_dict[pos_tail].remove(removed_from_tail)
        
        pos_paths = close_path_finder(data_manager, pos_head, pos_tail)
        if pos_paths != []:
            pos_reasoning_paths = "\n".join(
                " -> ".join(data_manager.triple_to_sentence(triple) for triple in path)
                for path in pos_paths
            )
            pos_reasoning_input = CLOSE_PATH_REASON_PROMPT.format(reasoning_paths=pos_reasoning_paths, test_triple=data_manager.triple_to_sentence(pos_triple))
        else:
            pos_known_triples = data_manager.open_path_finder(pos_triple)
            pos_reasoning_input = OPEN_PATH_REASON_PROMPT.format(known_triples="\n".join(pos_known_triples), test_triple=data_manager.triple_to_sentence(pos_triple))
        pos_reasoning_output = "Y"
        sft_instructions.append({"instruction": pos_reasoning_input, "input": "", "output": pos_reasoning_output})

        neg_samples = data_manager.neg_sampling(pos_triple, 3)
        for neg_triple in neg_samples:
            neg_paths = close_path_finder(data_manager, neg_triple[0], neg_triple[2])
            if neg_paths != []:
                neg_reasoning_paths = "\n".join(
                    " -> ".join(data_manager.triple_to_sentence(triple) for triple in path)
                    for path in neg_paths
                )
                neg_reasoning_input = CLOSE_PATH_REASON_PROMPT.format(reasoning_paths=neg_reasoning_paths, test_triple=data_manager.triple_to_sentence(neg_triple))
            else:
                neg_known_triples = data_manager.open_path_finder(neg_triple)
                neg_reasoning_input = OPEN_PATH_REASON_PROMPT.format(known_triples="\n".join(neg_known_triples), test_triple=data_manager.triple_to_sentence(neg_triple))
            neg_reasoning_output = "N"
            sft_instructions.append({"instruction": neg_reasoning_input, "input": "", "output": neg_reasoning_output})

        data_manager.entity2relationtail_dict[pos_head].append(removed_from_head)
        data_manager.entity2relationtail_dict[pos_tail].append(removed_from_tail)
                    
    sft_instructions_path = f"instructions/{dataset}/sft_instructions_train_size_{train_size}.json"
    with open(sft_instructions_path, "w", encoding="utf-8") as f:
        json.dump(sft_instructions, f, ensure_ascii=False, indent=4)
            
def main():
    parser = argparse.ArgumentParser(description='Process datasets with given hyperparameters')
    parser.add_argument("--dataset", type=str, choices=["FB15k-237-subset", "NELL-995-subset", "WN18RR-subset"], default="FB15k-237-subset")
    parser.add_argument("--train_size", type=str, choices=["full", "1000", "2000"], default="full", help="Size of the training data")

    args = parser.parse_args()
    build_instructions(args.dataset, args.train_size)

if __name__ == "__main__":
    main()