Bài Lab này tập trung vào kỹ thuật Digital Forensics (Điều tra số) đối với dữ liệu video. Mục tiêu chính là sử dụng phương pháp nhúng thủy vân bán dễ vỡ (Semi-fragile Watermarking) vào các hệ số DCT (Discrete Cosine Transform) để xác thực tính toàn vẹn và định vị vùng bị can thiệp trên video.

Hệ thống cho phép phát hiện các thay đổi dù là nhỏ nhất (như thay đổi 1 pixel) mà mắt thường không thể nhận ra, đồng thời khoanh vùng đỏ cảnh báo tại vị trí bị tấn công.
🚀 Hướng dẫn cài đặt và thực thi
1. Tải bài Lab về hệ thống
Mở Terminal trên máy ảo Labtainer Host và chạy các lệnh sau để clone repository từ GitHub:
Bash
cd ~/labtainer/trunk/labs
git clone https://github.com/TRuong08022004/lab.git video-forensics
2. Xây dựng môi trường (Build Lab)
Di chuyển sang thư mục scripts của Labtainer để đóng gói và cài đặt các thư viện cần thiết (OpenCV, FFmpeg):
Bash
cd ../scripts
./buildlab.py video-forensics
3. Bắt đầu thực hành
Chạy lệnh sau để khởi động container bài lab:
Bash
./labtainer video-forensics
📊 Quy trình thực hiện (Checkworks)
Task 1: Trích xuất vật chứng số (Checkwork 1)
Đây là bước chuẩn bị. Vì video được cấu thành từ nhiều frame ảnh, chúng ta cần tách video thành các frame để xử lý watermark trên từng khối pixel.

Thực hiện: Chạy script phân tích để lấy frame hình ảnh đầu tiên từ video gốc.

Lệnh: python3 bin/analyze_video.py

Kết quả: File data/frame_origin.png xuất hiện. Đây là "vật chứng sạch" dùng để niêm phong.

Task 2 & 3: Niêm phong bằng chứng - Watermarking (Checkwork 2-3)
Trong thực tế, để đảm bảo video không bị sửa, người ta phải "đánh dấu" nó ngay từ khi quay xong. Chúng ta sử dụng thuật toán nhúng thông tin vào miền tần số DCT.
Thực hiện: Chia ảnh thành các khối $8 \times 8$, tính toán mã băm (Hash) cho từng khối và nhúng chúng vào các hệ số DCT.
Lệnh: python3 bin/embed_auth.py
Kết quả: File data/watermarked_frame.png được tạo ra. Bằng mắt thường, ảnh này không khác gì ảnh gốc, nhưng bên trong nó đã chứa "niêm phong kỹ thuật số".

Task 4: Giả lập kịch bản tấn công (Checkwork 4)
Để kiểm tra xem hệ thống giám định có hoạt động hay không, chúng ta đóng vai kẻ tấn công thực hiện chỉnh sửa nội dung video.
Thực hiện: Sử dụng công cụ ffmpeg để vẽ một khối màu hoặc che đi một phần thông tin trên ảnh đã niêm phong.
Lệnh: ffmpeg -i data/watermarked_frame.png -vf "drawbox=x=100:y=100:w=50:h=50:color=black@1:t=fill" -y data/tampered_frame.png
Kết quả: Tạo ra data/tampered_frame.png. Lúc này, tính toàn vẹn của bằng chứng đã bị xâm phạm.

Task 5 & 6: Giám định pháp y và Khoanh vùng can thiệp (Checkwork 5-6)
Đây là công việc của một chuyên gia Điều tra số (Digital Forensics). Bạn sẽ sử dụng script để tìm ra những vị trí mà kẻ tấn công đã sửa đổi.
Thực hiện: Script sẽ quét lại toàn bộ ảnh nghi vấn, trích xuất watermark và so sánh mã Hash. Nếu mã Hash bị lệch dù chỉ 1 bit, vị trí đó sẽ bị đánh dấu.
Lệnh: python3 bin/detect_tamper.py
Kết quả: File data/detected_result.png xuất hiện với các ô vuông đỏ khoanh vùng chính xác vị trí bị can thiệp ở Task 4.

Task 7: Đánh giá độ tin cậy của hệ thống (Checkwork 7)
Một báo cáo giám định cần có số liệu cụ thể để trình trước hội đồng hoặc tòa án.

Thực hiện: Tính toán các chỉ số Accuracy (Độ chính xác) và tỷ lệ Báo động giả (False Positive).

Lệnh: python3 bin/evaluate.py

Kết quả: Một file log reports/evaluation.log chứa các con số thống kê. Nếu Accuracy đạt ~100%, hệ thống giám định của bạn cực kỳ đáng tin cậy.
