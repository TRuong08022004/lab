import cv2
import numpy as np
import hashlib
from scipy.fftpack import dct, idct

def get_hash_bit(block):
    """Checkwork 2: Sinh Authentication Watermark từ Hash của Block"""
    m = hashlib.sha256()
    m.update(block.tobytes())
    # Lấy byte đầu tiên của mã Hash, chuyển sang bit cuối cùng (LSB)
    return int(bin(m.digest()[0])[-1])

def embed_watermark(image_path, output_path):
    # Đọc ảnh gốc
    img = cv2.imread(image_path)
    if img is None:
        print("Không tìm thấy ảnh!")
        return

    # Chuyển sang hệ màu YCrCb để nhúng vào kênh Y (Luminance)
    # Giúp watermark khó bị phát hiện bằng mắt thường hơn
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    y_channel = ycrcb[:,:,0].astype(np.float32)
    h, w = y_channel.shape

    # Checkwork 3: Nhúng Semi-fragile Watermark vào DCT
    # Duyệt qua từng block 8x8
    for i in range(0, h - 8 + 1, 8):
        for j in range(0, w - 8 + 1, 8):
            block = y_channel[i:i+8, j:j+8]
            
            # Tính bit xác thực từ chính dữ liệu block này
            auth_bit = get_hash_bit(block.astype(np.uint8))
            
            # Biến đổi DCT 2 chiều
            dct_block = cv2.dct(block)
            
            # Chọn hệ số DCT tại vị trí (3,3) - Tần số trung bình
            # Vị trí này đủ nhạy để hỏng khi bị sửa nội dung (fragile)
            val = dct_block[3, 3]
            
            # Kỹ thuật nhúng: QIM (Quantization Index Modulation) đơn giản
            # Nếu bit=1: làm tròn val thành số lẻ gần nhất
            # Nếu bit=0: làm tròn val thành số chẵn gần nhất
            step = 1 # Bước lượng tử hóa
            quantized = round(val / step)
            
            if auth_bit == 1:
                if quantized % 2 == 0: quantized += 1
            else:
                if quantized % 2 != 0: quantized -= 1
            
            dct_block[3, 3] = quantized * step
            
            # Nghịch đảo DCT để đưa về miền không gian (pixel)
            y_channel[i:i+8, j:j+8] = cv2.idct(dct_block)

    # Ghép lại các kênh màu và lưu ảnh
    ycrcb[:,:,0] = np.clip(y_channel, 0, 255)
    final_img = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
    cv2.imwrite(output_path, final_img)
    print(f"Đã nhúng xong! File lưu tại: {output_path}")

if __name__ == "__main__":
    embed_watermark('data/frame_origin.png', 'data/watermarked_frame.png')
