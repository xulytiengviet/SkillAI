---
name: quy-hoach-kmz-osm
description: Tạo lớp phủ bản đồ quy hoạch KML/KMZ cho Google Earth từ ảnh hoặc PDF, tự georeference theo sông/kênh và đường OpenStreetMap, kiểm tra sai số và xuất KMZ có nguồn. Dùng khi người dùng yêu cầu đưa bản đồ quy hoạch lên Google Earth, tạo KMZ quy hoạch, căn chỉnh ảnh quy hoạch theo OSM, hoặc georeference bản đồ quy hoạch Việt Nam.
---

# Quy hoạch → KMZ Google Earth, tự khớp OSM

Biến ảnh/PDF bản đồ quy hoạch thành lớp phủ KMZ đặt đúng vị trí trên Google Earth. Ưu tiên tự động và chỉ chấp nhận kết quả sau khi kiểm tra các mốc độc lập.

## Đầu ra bắt buộc
- `*.kmz`: GroundOverlay cho Google Earth.
- `*_params.json`: tham số georeference.
- `*_check.jpg`: ảnh kiểm tra có sông/đường OSM chồng lên bản quy hoạch.
- `*_boundary.kml` nếu yêu cầu theo đơn vị hành chính.
- Báo cáo nguồn, cách khớp, m/px, score/residual và cảnh báo sai số.

KMZ chỉ là lớp tham khảo không gian, không thay hồ sơ quy hoạch/địa chính pháp lý.

## 1. Nguồn
Nếu người dùng đã gửi file/link thì dùng ngay. Nếu chỉ nêu địa danh/đồ án, tìm nguồn công bố chính thức trước. Ưu tiên cơ quan nhà nước, quyết định/phụ lục, rồi báo chí chính thống đăng lại bản gốc. Không lấy My Maps/lớp cá nhân khi không có quyền sử dụng.

## 2. Chuẩn hóa ảnh
Với PDF, render đúng trang bản đồ, cạnh dài khoảng 5000–7000 px. Che khung tên, chú giải, bảng thống kê và sơ đồ phụ:
```bash
python scripts/qh_overlay.py grid INPUT.jpg --out grid.jpg
python scripts/qh_overlay.py masks INPUT.jpg --exclude "x0,y0,x1,y1;..." --out masks.png
```

## 3. Tải OSM
```bash
python scripts/qh_overlay.py geocode "<địa danh>, Việt Nam" --margin-km 4
python scripts/qh_overlay.py fetch-osm --bbox S,W,N,E --out osm.json
```
Bbox phải phủ toàn bộ tờ bản đồ.

## 4. Khớp hai tầng

### A. Sông/kênh/mặt nước
```bash
python scripts/qh_overlay.py align INPUT.jpg --osm osm.json --exclude "..." --out params.json --check check.jpg
```
Thuật toán tìm phép đồng dạng (tịnh tiến + tỉ lệ + xoay), ưu tiên hình dạng mặt nước.
- score >= 0.60: ứng viên tốt, vẫn phải xem check.
- 0.50–0.60: cần xác nhận bằng đường hiện hữu.
- < 0.50: không tự chấp nhận, chuyển sang GCP.

### B. Đường/giao lộ OSM làm GCP
Dùng khi mặt nước yếu, khớp sai hoặc cần bám đường chính.
1. Chọn 3–5 nút giao/cầu hiện hữu, trải đều; tránh đường chỉ có trong quy hoạch tương lai.
2. Lấy tọa độ giao hai đường có tên:
```bash
python scripts/qh_overlay.py intersect --osm osm.json --road1 "Đường A" --road2 "Đường B"
```
3. Dùng khả năng nhìn ảnh của ChatGPT để xác định pixel (u,v) của cùng mốc trên bản đồ.
4. Chạy:
```bash
python scripts/qh_overlay.py align INPUT.jpg --osm osm.json --exclude "..."   --gcp "u1,v1,lat1,lon1;u2,v2,lat2,lon2;u3,v3,lat3,lon3"   --refine --out params.json --check check.jpg
```
Loại GCP có residual bất thường và chạy lại. Ưu tiên nghiệm khớp đồng thời sông và đường.

## 5. Ranh giới tham chiếu
```bash
python scripts/qh_overlay.py boundary --bbox S,W,N,E --name "<tên đơn vị>" --out khu_vuc_boundary.kml
```
Không coi ranh OSM là ranh pháp lý nếu chưa có nguồn hành chính chính thức.

## 6. Xuất KMZ
```bash
python scripts/qh_overlay.py export --params params.json --osm osm.json   --name "<Tên đồ án>"   --desc "Nguồn: <cơ quan/link>; Quyết định: <nếu có>; Georeference: OSM sông/đường; chỉ tham khảo"   --out quy_hoach_overlay.kmz
```

## 7. Verify
```bash
python scripts/qh_overlay.py verify --kmz quy_hoach_overlay.kmz --kml khu_vuc_boundary.kml --out verify.jpg
```
Kiểm tra ít nhất bờ sông/cầu, trục đường/giao lộ và một mốc độc lập khác. Nếu một vùng khớp nhưng vùng khác lệch có hệ thống, ảnh có thể méo phi tuyến; báo hạn chế và đề nghị affine/projective/TPS trong GIS thay vì ép phép đồng dạng.

## Quy tắc
- Không đoán vị trí khi thiếu bbox/mốc.
- Không dùng đường quy hoạch mới làm GCP với OSM hiện trạng.
- Không chấp nhận score thấp chỉ vì nhìn có vẻ đúng.
- Không cắt lẹm bản đồ khi che chú giải.
- Ảnh vệ tinh chỉ để kiểm tra nếu giấy phép không cho nhúng lại.
- Ghi attribution OpenStreetMap khi dùng dữ liệu OSM.
- Khi trả kết quả, nêu file KMZ, nguồn, phương pháp khớp, số GCP/residual, m/px, score và cảnh báo pháp lý.

Tài nguyên: `scripts/qh_overlay.py`, `references/algorithm.md`, `references/chatgpt-usage.md`, `LICENSE.txt`.
