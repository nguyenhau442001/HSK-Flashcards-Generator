#!/bin/bash
# tools/run_after_delay.sh
# Tự động chờ Google reset quota và tiếp tục chạy pipeline tạo ảnh minh họa

DELAY_HOURS=${1:-9.6}
DELAY_SECONDS=$(python3 -c "print(int(float('$DELAY_HOURS') * 3600))")

echo "=========================================================="
echo "  HSK Illustration Pipeline - Scheduled Delayed Runner"
echo "  Thời gian chờ: $DELAY_HOURS giờ (~$DELAY_SECONDS giây)"
echo "  Bắt đầu chạy lúc: $(date)"
echo "  Dự kiến khởi động lại lúc: $(date -v+${DELAY_SECONDS}s '+%Y-%m-%d %H:%M:%S')"
echo "=========================================================="

sleep $DELAY_SECONDS

echo ""
echo "[*] Đã hết thời gian chờ! Bắt đầu chạy pipeline tạo ảnh mới..."
cd "$(dirname "$0")/.." || exit 1
python3 tools/batch_generate_all.py --delay 3.5 --batch-size 10
