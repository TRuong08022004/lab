import cv2
import numpy as np
import hashlib

def get_hash_bit(block):
    m = hashlib.sha256()
    m.update(block.tobytes())
    return int(bin(m.digest()[0])[-1])

def detect_tamper(image_path, output_path):
    img = cv2.imread(image_path)
    if img is None: return

    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    y_channel = ycrcb[:,:,0].astype(np.float32)
    h, w = y_channel.shape
    
    # Tạo một bản sao để vẽ vùng bị cảnh báo
    result_img = img.copy()
    tamper_count = 0

    for i in range(0, h - 8 + 1, 8):
        for j in range(0, w - 8 + 1, 8):
            block = y_channel[i:i+8, j:j+8]
            
            # 1. Trích xuất bit đã nhúng từ hệ số DCT [3,3]
            dct_block = cv2.dct(block)
            val = dct_block[3, 3]
            extracted_bit = int(round(val)) % 2
            
            # 2. Tính toán lại bit Hash từ dữ liệu pixel hiện tại
            current_hash_bit = get_hash_bit(block.astype(np.uint8))
            
            # 3. So sánh (Phát hiện can thiệp)
            if extracted_bit != current_hash_bit:
                # Nếu sai lệch, tô đỏ block đó (Checkwork 6: Visualization)
                tamper_count += 1
                cv2.rectangle(result_img, (j, i), (j+8, i+8), (0, 0, 255), 1)

    cv2.imwrite(output_path, result_img)
    print(f"Phát hiện {tamper_count} block bị chỉnh sửa!")
    print(f"Kết quả Forensic lưu tại: {output_path}")

if __name__ == "__main__":
    detect_tamper('data/tampered_frame.png', 'data/detected_result.png')
