# Thuật toán georeference

Skill dùng phép đồng dạng 2D:
`u = cx + s(cos(r)*x - sin(r)*y)`
`v = cy + s(sin(r)*x + cos(r)*y)`

Trong đó x/y là mét cục bộ, u/v là pixel, s là pixel/mét, r là góc xoay.

## Mặt nước
Ảnh quy hoạch được phân nhóm nước/đất bằng màu. OSM lấy polygon `natural=water`, `waterway=riverbank` và line river/canal/stream có buffer. Thuật toán tìm scale/rotation/translation có tương quan tốt nhất giữa mask nước ảnh và OSM, đồng thời phạt OSM rơi vào mask đất.

## Đường/GCP
Đường OSM được vẽ lên ảnh kiểm tra và dùng làm điểm khống chế khi mặt nước yếu. Ưu tiên motorway/trunk/primary/secondary hiện hữu, cầu và nút giao lớn. Dùng 3–5 GCP trải đều để phát hiện điểm ngoại lai qua residual.

## Giới hạn
Nếu residual tăng theo vị trí hoặc một góc khớp nhưng góc đối diện lệch mạnh, ảnh có thể bị chụp xiên/scan co kéo/ghép ảnh. Khi đó cần affine/projective/polynomial/TPS bằng QGIS/GDAL.

Score mặt nước chỉ là thước đo tương đối; độ chính xác mét phải đánh giá bằng residual GCP và các mốc độc lập.
