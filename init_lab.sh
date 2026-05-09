#!/bin/bash
# Script khởi tạo Lab Video Forensics - Trần Bá Trường (B22DCAT308)

LAB_NAME="video-forensics"
LAB_DEST="$HOME/labtainer/trunk/labs/$LAB_NAME"

echo "------------------------------------------"
echo "🚀 Đang cấu hình bài Lab: $LAB_NAME"
echo "------------------------------------------"

# 1. Tạo thư mục và đồng bộ dữ liệu vào Labtainer Trunk
mkdir -p $LAB_DEST
cp -r config/ $LAB_DEST/
cp -r instr_config/ $LAB_DEST/
cp -r dockerfiles/ $LAB_DEST/
cp -r video-forensics/ $LAB_DEST/

# 2. Build lại Image Docker sạch
echo "📦 Đang build môi trường Docker..."
cd $LAB_DEST/dockerfiles
docker build -t $LAB_NAME.$LAB_NAME.student -f Dockerfile.$LAB_NAME.student .

# 3. Chạy Lab
echo "🏁 Hoàn tất! Đang khởi động Lab..."
cd $HOME/labtainer/labtainer-student
./labtainer $LAB_NAME -r
