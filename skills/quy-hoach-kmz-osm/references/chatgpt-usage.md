# Cài và dùng trong ChatGPT / OpenAI

## ChatGPT
Nếu workspace hỗ trợ Skills, vào Plugins → Skills → Create/Upload và tải gói ZIP của skill lên.

Prompt mẫu:
- "Dùng skill quy-hoach-kmz-osm, biến PDF này thành KMZ Google Earth và tự khớp theo sông/đường OSM."
- "Nếu sông không đủ mạnh, tự dùng 3–5 giao lộ OSM làm GCP."
- "Kiểm tra KMZ này có lệch so với OSM không và tạo ảnh verify."

## OpenAI API
Gói ZIP phải chứa đúng một thư mục top-level của skill và đúng một `SKILL.md`.

## Python
Cần Python >= 3.9 và:
```bash
python -m pip install -r requirements.txt
```
