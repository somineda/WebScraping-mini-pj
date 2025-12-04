import re

import httpx
from bs4 import BeautifulSoup

from app.models import Quote

#명언 스크래핑 후 디비에 저장
async def scrape_and_save_quotes(pages: int = 10):
    base_url = "https://saramro.com/quotes"
    saved_count = 0

    async with httpx.AsyncClient() as client:
        for page in range(1, pages + 1):
            try:
                response = await client.get(f"{base_url}?page={page}")
                soup = BeautifulSoup(response.text, "html.parser")

                rows = soup.select("table tbody tr")

                for row in rows:
                    #명언 내용이 있는 행 (colspan="5"인 td)
                    content_td = row.select_one("td[colspan='5']")
                    if content_td:
                        #전체 텍스트 가져오기
                        raw_text = content_td.get_text(separator="\n", strip=True)

                        #작가 추출 (- 또는 — 뒤에 오는 이름)
                        author = None
                        author_match = re.search(r"[-–—]\s*([가-힣A-Za-z.\s]+)$", raw_text, re.MULTILINE)
                        if author_match:
                            author = author_match.group(1).strip()

                        #명언 내용 추출 (첫 번째 줄 또는 - 앞까지)
                        lines = raw_text.split("\n")
                        content = lines[0].strip()

                        #내용이 너무 짧거나 없으면 스킵
                        if len(content) < 5:
                            continue

                        #중복 체크 후 저장
                        exists = await Quote.filter(content=content).exists()
                        if not exists:
                            await Quote.create(content=content, author=author)
                            saved_count += 1

            except Exception as e:
                print(f"Error scraping page {page}: {e}")
                continue

    total_count = await Quote.all().count()
    return {
        "message": f"Scraping completed. Saved {saved_count} new quotes. Total: {total_count}"
    }