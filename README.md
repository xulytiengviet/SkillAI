# SkillAI — Quy hoạch KMZ + OpenStreetMap

Skill dành cho ChatGPT/OpenAI để biến ảnh hoặc PDF bản đồ quy hoạch thành **lớp phủ KMZ cho Google Earth**, tự căn chỉnh theo **sông/kênh và đường OpenStreetMap**.

## Skill chính

`skills/quy-hoach-kmz-osm/`

Khả năng:
- nhận ảnh/PDF bản đồ quy hoạch;
- geocode khu vực và tải sông/đường/mặt nước OSM;
- tự khớp theo mặt nước;
- khi mặt nước yếu, dùng đường/giao lộ OSM làm GCP và tinh chỉnh;
- xuất GroundOverlay KMZ nền trong suốt;
- tạo ảnh kiểm tra với OSM/vệ tinh;
- kèm nguồn, tham số georeference và cảnh báo sai số.

## Cấu trúc

```text
SkillAI/
├─ skills/
│  └─ quy-hoach-kmz-osm/
│     ├─ SKILL.md
│     ├─ LICENSE.txt
│     ├─ requirements.txt
│     ├─ scripts/qh_overlay.py
│     └─ references/
│        ├─ algorithm.md
│        └─ chatgpt-usage.md
└─ dist/
   └─ quy-hoach-kmz-osm.zip
```

## Cài vào ChatGPT

Theo tài liệu OpenAI hiện hành, một Skill là thư mục có `SKILL.md` và có thể kèm scripts/references. Gói ZIP trong `dist/` chứa **một thư mục top-level duy nhất** và một `SKILL.md`, phù hợp để upload vào giao diện Skills hoặc API hỗ trợ Skills.

## Chạy script độc lập

```bash
cd skills/quy-hoach-kmz-osm
python -m pip install -r requirements.txt
python scripts/qh_overlay.py -h
```

Ví dụ:

```bash
python scripts/qh_overlay.py geocode "phường An Khánh, TP Hồ Chí Minh" --margin-km 4
python scripts/qh_overlay.py fetch-osm --bbox 10.735,106.690,10.835,106.820 --out osm.json
python scripts/qh_overlay.py align map.jpg --osm osm.json --out params.json --check check.jpg
python scripts/qh_overlay.py export --params params.json --osm osm.json --name "Quy hoạch" --out quy-hoach.kmz
```

## Ghi công

Phần lõi `qh_overlay.py` được tích hợp từ dự án MIT của **thieprealtor**: `thieprealtor/ban-do-quy-hoach-overlay`. Bản tích hợp Skill/README/quy trình ChatGPT do **Long Ngo / xulytiengviet** thực hiện và giữ nguyên ghi công upstream theo MIT.

## Lưu ý

KMZ tạo ra là lớp tham khảo trực quan. Không dùng nó thay thế hồ sơ quy hoạch, bản đồ địa chính hoặc xác nhận pháp lý của cơ quan có thẩm quyền.
