import requests
from datetime import datetime, timezone

# Địa chỉ API
api_url = "https://scholar-pcrawler-1.elemarkuspet.repl.co/get_paper/YpOO60MAAAAJ"

# Lấy dữ liệu từ API
response = requests.get(api_url)
data = response.json()

# Lấy ngày, tháng, năm và múi giờ hiện tại
current_datetime = datetime.now(timezone.utc)
current_date_time_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S %Z")

# Tạo chuỗi HTML từ dữ liệu và thêm thông tin thời gian
html_content = "\n\n<table id=\"scholar-table\" style=\"position: relative;\">\n"
html_content += "  <tr>\n"
html_content += "    <th>Title</th>\n"
html_content += "    <th>Authors</th>\n"
html_content += "    <th>Citations</th>\n"
html_content += "    <th>Year</th>\n"
html_content += "  </tr>\n"

for paper in data["papers"]:
    html_content += (
        f"  <tr>\n    <td><a href=\"{paper['Paper_URL']}\">{paper['Title']}</a></td>\n"
        f"    <td>{paper['Authors']}</td>\n    <td>{paper['Citations']}</td>\n"
        f"    <td>{paper['Year']}</td>\n  </tr>\n"
    )

# Add the "Show more" row with center alignment, larger font size, and italicized text
html_content += f"  <tr>\n    <td colspan=\"4\" id=\"show-more-cell\" "
html_content += f"style=\"text-align:center; font-size: larger; position: relative;\" "
html_content += f"title=\"Last Updated: {current_date_time_str}\">\n"
html_content += f"<em><a href=\"{data['user_scholar_url']}\" style=\"display: inline-block;\">Show more</a></em></td>\n  </tr>\n</table>\n"

# Đọc toàn bộ README.md
with open("README.md", "r", encoding="utf-8") as readme_file:
    readme_content = readme_file.read()

# Tìm vị trí bắt đầu và kết thúc của phần cần thay thế
start_marker = "<!-- SCHOLAR-LIST:START -->"
end_marker = "<!-- SCHOLAR-LIST:END -->"
start_pos = readme_content.find(start_marker) + len(start_marker)
end_pos = readme_content.find(end_marker)

# Thay thế phần giữa start_pos và end_pos bằng nội dung mới của bảng và thông tin thời gian
new_readme_content = (
    readme_content[:start_pos] + html_content + readme_content[end_pos:]
)

# Ghi nội dung mới vào README.md
with open("README.md", "w", encoding="utf-8") as readme_file:
    readme_file.write(new_readme_content)


# Create an SVG file and embed HTML content
svg_content = f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
svg_content += f'<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">\n'
svg_content += f'  <foreignObject width="100%" height="100%">\n'
svg_content += f'    <div xmlns="http://www.w3.org/1999/xhtml">\n'
svg_content += html_content
svg_content += f'    </div>\n'
svg_content += f'  </foreignObject>\n'
svg_content += f'</svg>\n'

# Save the SVG content to a file
with open("output.svg", "w", encoding="utf-8") as svg_file:
    svg_file.write(svg_content)