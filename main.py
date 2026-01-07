import asyncio
from fastapi import FastAPI
from playwright.async_api import async_playwright
from fastapi import HTTPException
import pandas as pd
import os

def main():
    print("Hello from technical-assessment!")

app = FastAPI()

base_url = "https://bizfileonline.sos.ca.gov/search/business"
max_records = 500

@app.get("/search")
async def search_busness(term: str, page_number: int = 0, limit: int = 10):
    csv_name = f"{term}_business_data.csv"
    
    if os.path.exists(csv_name):
        try:
            df = pd.read_csv(csv_name)
            results = df.to_dict('records')

            return {
                "count" : len(results[page_number * limit : (page_number + 1) * limit]),
                "csv_saved" : csv_name,
                "data" : results[page_number * limit : (page_number + 1) * limit],
                "page": page_number,
                "total_pages": (len(results) + limit - 1) // limit,
                "from_cache": True
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading the file: {e}")

    async with  async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            ignore_https_errors=True,
        )


        page = await context.new_page()

        await page.set_extra_http_headers({
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/",
        })
        

        results = []

        try: 
            await page.goto(base_url, wait_until="load", timeout=30000)
            
            print(await page.content())

            search = page.locator("input.search-input")

            await search.wait_for(state="visible", timeout=60000)
            await search.fill(term)
            await search.press("Enter")


            await page.wait_for_selector(".div-table-body", timeout=60000)

            while len(results) < max_records:
                rows = await page.locator('.div-table-row').all()
            
                for row in rows:
                    if len(results) >= max_records:
                        break

                    cells = row.locator(".div-table-cell")
                    if await cells.count() < 4:
                        continue

                    record = {
                        "entity_number": await cells.nth(0).inner_text(),
                        "date": await cells.nth(1).inner_text(),
                        "status": await cells.nth(2).inner_text(),
                        "entity_name": await cells.nth(3).inner_text(),
                        "agent": await cells.nth(4).inner_text(),
                    }
                    results.append(record)

            df = pd.DataFrame(results)
            df.to_csv(csv_name, index=False)

            return {
                "count" : len(results[page_number * limit : (page_number + 1) * limit]),
                "csv_saved" : csv_name,
                "data" : results[page_number * limit : (page_number + 1) * limit],
                "page": page_number,
                "total_pages": (len(results) + limit - 1) // limit,
                "from_cache": False
            }
    
        except Exception as e:
            content = await page.content()
            print(content)
            raise HTTPException(status_code=500, detail=f"Error: {e}")
    
        finally:
            await browser.close()