# CATS: Context-aware Inductive Knowledge Graph Completion with Latent Type Constraints and Subgraph Reasoning

This repository provides the official implementation of the paper *"Context-aware Inductive Knowledge Graph Completion with Latent Type Constraints and Subgraph Reasoning"* (To appear in AAAI2025).

![CATS](CATS.png)

## Environment Setup

Please follow these steps to execute our code:

1. **Install dependencies:**
   Create a python environment and install the required packages. We suggest you use Python 3.10 with PyTorch 2.2.2.
   For detailed Python package versions, you may refer to the suggested settings listed in `requirements.txt` from [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory/blob/main/requirements.txt). 

   ```bash
   pip install -r requirements.txt
   ```
   
   Additionally, install `sentence_transformers`:

   ```bash
   pip install sentence_transformers
   ```

## Dataset

Download the full dataset and LLM instructions from the following link:

- [Dataset &amp; Instructions](https://drive.google.com/drive/folders/17C3BsllCWy_TK3B5WwCjxPQo2heuLJPz?usp=drive_link)

Alternatively, you can construct the LLM instruction prompts by executing `python build_instruction.py`.

## LLM Setup

You may download LLM checkpoints from the following links:
Our experimental results can be reproduced with the Qwen2-7B-Instruct LLM. 

- [Qwen2-7B-Instruct](https://huggingface.co/Qwen/Qwen2-7B-Instruct)
- [Meta-Llama-3-8B-Instruct](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct)

Please update the default value of `LLM_PATH` in script `data_manager.py` with your local model path.

## Intruction-tuning

Please refer to the official document of [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory/) for supervised fine-tuning with the provided prompts. Hyper-parameters are provided in our paper. 

## Inference

To evaluate the model performance, execute the following command:

```bash
python3 prediction.py --dataset FB15k-237-subset --setting inductive --training_size full --model_name {model_path_after_sft} --prompt_type CATS --subgraph_type together --path_type degree
```

