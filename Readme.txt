vlsp sem parsing run code

* Lưu ý: trong thư mục submit-data đi kèm đã có sẵn các file output infer từ mô hình của nhóm, submit-data/output_private_27_58.txt, đây là file đạt kết quả 0.58 trên AIHub sau khi đã qua post-process. file submit-data/output.txt tương đương với file trên, được đổi tên thuận tiện cho việc chạy các đoạn code python dưới đây.

Mô hình đã finetune và sử dụng cho kết quả 0.58 trên AIHub private
    - ICTuniverse/unsloth-Qwen3-14B-unsloth-bnb-4bit-finetuned (model trên hugging face).

preprocessing data for training (start with original data)

1. merge 2 files (merge 2 file train_amr_1 và train_amr_2.txt)
python merge_train.py -f original-data/train_amr_1.txt original-data/train_amr_2.txt -o original-data/train_amr_merged.txt

2. preprocess amr graph
python var_remove_amr.py -f original-data/train_amr_merged.txt -o processed-data/amr_graph_processed.txt

3. fix auto new line error
python fix_auto_next_line.py -f processed-data/amr_graph_processed.txt

4. merge with snt
python merge_problems_with_graph.py --original-file original-data/train_amr_merged.txt --processed-file processed-data/amr_graph_processed.txt.joined --output-path processed-data/train_processed.txt

sau bước này, sẽ thu được file “train_processed.txt”.

post-processing data after inferring model.

sau khi infer, notebook infer_task_9_qwen_private.ipynb sẽ trả về file "output.txt"
1. extract amr graph and snt into 2 files
python split_snt_amr.py submit-data/output.txt

2. postprocess amr graph
python postprocess_AMRs.py -f submit-data/graphs_only.txt -s submit-data/problems_only.txt

3. merge with snt file
python merge_problems_with_graph.py --original-file submit-data/output.txt --processed-file submit-data/graphs_only.txt.restore --output-path submit-data/final.txt

sau bước này, sẽ thu được file “final.txt” là file sử dụng để submit (lưu ý, đổi tên về results.txt, sau đó zip, thành results.zip)

* Các notebook sử dụng:
    * finetune_qwen_task_9.ipynb: sử dụng với mục đích fine-tune mô hình qwen3-14B của unsloth
    * infer_task_9_qwen.ipynb: sử dụng với mục đích infer mô hình cho public test.
    * infer_task_9_qwen_private.ipynb: sử dụng với mục đích infer mô hình cho private test.
        * Lưu ý: cài đặt siêu tham số temperature=0.6

* Mô hình trong notebook finetune: unsloth/Qwen3-14B-unsloth-bnb-4bit
* Mô hình trong notebook infer, model đã finetun: ICTuniverse/unsloth-Qwen3-14B-unsloth-bnb-4bit-finetuned




