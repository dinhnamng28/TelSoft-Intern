from TikTokApi import TikTokApi

# Khởi tạo trong chế độ browser (bắt buộc với search)
with TikTokApi() as api:
    keyword = "bitcoin"

    # Lấy 10 video đầu tiên theo từ khóa
    results = api.search_results(keyword, count=10)

    for i, video in enumerate(results, 1):
        print(f"\n--- Video {i} ---")
        print(f"ID: {video['id']}")
        print(f"Description: {video['desc']}")
        print(f"Author: {video['author']['uniqueId']}")
        print(f"Views: {video['stats']['playCount']}")
        print(f"Likes: {video['stats']['diggCount']}")
        print(f"Comments: {video['stats']['commentCount']}")
        print(f"Shares: {video['stats']['shareCount']}")
        print(f"URL: https://www.tiktok.com/@{video['author']['uniqueId']}/video/{video['id']}")
