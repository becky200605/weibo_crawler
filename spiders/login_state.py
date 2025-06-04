from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://weibo.com")
    
    input("✅ 请扫码登录后，按回车键继续...")

    context.storage_state(path="storage/weibo_login_state.json")
    print("✅ 登录状态已保存到 weibo_login_state.json")
    browser.close()