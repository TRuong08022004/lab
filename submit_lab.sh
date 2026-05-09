#!/bin/bash
# Script đóng gói kết quả nộp bài - B22DCAT308

LAB_NAME="video-forensics"
MSV="B22DCAT308"
TIME_STAMP=$(date +%Y%m%d_%H)

echo "🛠️ Đang dừng Lab và đóng gói kết quả..."

# 1. Dừng lab
cd $HOME/labtainer/labtainer-student
./stoplab $LAB_NAME

# 2. Thu thập và đổi tên file kết quả
XFER_PATH="$HOME/labtainer_xfer/$LAB_NAME"
LATEST_ZIP=$(ls -t $XFER_PATH/*.zip | head -1)

if [ -f "$LATEST_ZIP" ]; then
    NEW_NAME="${MSV}_${LAB_NAME}_${TIME_STAMP}.zip"
    cp "$LATEST_ZIP" "$HOME/Desktop/$NEW_NAME"
    echo "------------------------------------------"
    echo "✅ THÀNH CÔNG! File nộp bài đã được tạo tại Desktop:"
    echo "👉 $NEW_NAME"
    echo "------------------------------------------"
else
    echo "❌ Lỗi: Không tìm thấy file kết quả zip."
fi
