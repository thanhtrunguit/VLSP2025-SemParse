
from amr import AMR

def multiline_to_oneline(text: str) -> str:
    return " ".join(line.strip() for line in text.strip().splitlines())

def parse_amr_no_check(amr_multiline: str):
    try:
        amr_line = multiline_to_oneline(amr_multiline)
        amr = AMR.parse_AMR_line(amr_line)
        return amr
    except Exception:
        return None

input_file = "errors/results.txt"  # Tên file đầu vào chứa AMR

with open(input_file, "r", encoding="utf-8") as fin:
    buffer = []
    sentence_line = ""

    for line in fin:
        if line.startswith("#::snt"):
            # Khi thấy câu mới thì xử lý đoạn AMR cũ
            if buffer:
                amr_text = "".join(buffer)
                amr = parse_amr_no_check(amr_text)
                if not amr:
                    print(f"❌ Lỗi parse ở câu: {sentence_line.strip()}")
                buffer = []
            sentence_line = line  # Lưu lại dòng câu
        elif line.strip():
            buffer.append(line)

    # Xử lý đoạn cuối cùng trong file
    if buffer:
        amr_text = "".join(buffer)
        amr = parse_amr_no_check(amr_text)
        if not amr:
            print(f"❌ Lỗi parse ở câu: {sentence_line.strip()}")

print("✅ Đã kiểm tra xong.")
