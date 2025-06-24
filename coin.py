# import requests
# import json

# # Gọi API chi tiết coin
# url = "https://api.coingecko.com/api/v3/coins/ethereum"
# response = requests.get(url)
# def get_first_item(lst):
#     return lst[0] if lst and len(lst) > 0 else "Không có"


# # Kiểm tra trạng thái
# if response.status_code == 200:
#     data = response.json()
    
#     # In ra các thông tin chung
#     print("=== THÔNG TIN CHUNG CỦA COIN ===")
#     print("ID:", data.get("id"))
#     print("Tên:", data.get("name"))
#     print("Ký hiệu:", data.get("symbol"))
#     print("Ngày tạo (Genesis Date):", data.get("genesis_date"))
#     print("Thuật toán băm:", data.get("hashing_algorithm"))
#     print("Thời gian tạo block (phút):", data.get("block_time_in_minutes"))
#     print("Quốc gia phát hành:", data.get("country_origin"))
#     print("Danh mục:", ", ".join(data.get("categories", [])))

#     print("\n=== LIÊN KẾT ===")
#     print("Website:", get_first_item(data["links"]["homepage"]))
#     print("Blockchain Explorer:", get_first_item(data["links"]["blockchain_site"]))
#     print("Forum:", get_first_item(data["links"]["official_forum_url"]))
#     print("Chat:", get_first_item(data["links"]["chat_url"]))
#     print("Twitter:", data["links"].get("twitter_screen_name", "Không có"))
#     print("Subreddit:", data["links"].get("subreddit_url", "Không có"))

#     print("\n=== HÌNH ẢNH ===")
#     print("Logo nhỏ:", data["image"]["thumb"])
#     print("Logo lớn:", data["image"]["large"])

#     print("\n=== CẢM XÚC CỘNG ĐỒNG ===")
#     print("Up vote (%):", data.get("sentiment_votes_up_percentage"))
#     print("Down vote (%):", data.get("sentiment_votes_down_percentage"))
#     print("Số người theo dõi:", data.get("watchlist_portfolio_users"))

#     print("\n=== MÔ TẢ ===")
#     print(data["description"]["en"], "...")  # In 500 ký tự đầu

# else:
#     print("Lỗi khi gọi API:", response.status_code)


import requests

# Gọi API từ CoinGecko
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "ids": "bitcoin"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()[0]  # Chỉ lấy thông tin của Bitcoin

    print("====== Thông tin thị trường Bitcoin ======")
    print(f"ID: {data.get('id')}")
    print(f"Symbol (Ký hiệu): {data.get('symbol')}")
    print(f"Tên: {data.get('name')}")
    print(f"Giá hiện tại: {data.get('current_price')} USD")
    print(f"Tổng vốn hóa thị trường: {data.get('market_cap')}")
    print(f"Thứ hạng vốn hóa: {data.get('market_cap_rank')}")
    print(f"Tổng khối lượng giao dịch 24h: {data.get('total_volume')}")
    print(f"Giá cao nhất 24h: {data.get('high_24h')} USD")
    print(f"Giá thấp nhất 24h: {data.get('low_24h')} USD")
    print(f"Biến động giá 24h: {data.get('price_change_24h')} USD")
    print(f"Phần trăm biến động 24h: {data.get('price_change_percentage_24h')}%")
    print(f"Lượng cung đang lưu hành: {data.get('circulating_supply')}")
    print(f"Tổng cung: {data.get('total_supply')}")
    print(f"Cung tối đa: {data.get('max_supply')}")
    print(f"Giá cao nhất mọi thời đại (ATH): {data.get('ath')} USD")
    print(f"Giá thấp nhất mọi thời đại (ATL): {data.get('atl')} USD")
    print(f"Thời gian cập nhật cuối cùng: {data.get('last_updated')}")
else:
    print("Lỗi khi gọi API:", response.status_code)
