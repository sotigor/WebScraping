from playwright.sync_api import Playwright, sync_playwright
from extra_functions import *
from locators import *

def start_scraping(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://epicentrk.ua/shop/")
    page.get_by_text("КиевКиев, ул. Полярная, 20-Д").first.click()
    page.get_by_text("ТЦ «Эпицентр»Киев, пр-т С. Бандеры, 11-А5 км044 428 90 40Пн-вс:08:00 — 21:00ЦЕНТ").click()
    page.locator(".header__burger").click()
    page.locator("//a[@title = 'Электроника']").click()
    page.get_by_role("link", name="Смартфоны").click()
    page.locator("//div[@class='button-group27 show-for-large']/a[4]").click()
    page.locator("[alt='Tecno']").click()
    number_of_pages = get_quantity_of_pagination_pages(page, PAGINATION_ITEM_LOCATOR)
    get_lists_of_smartphones_and_prices(page, MODEL_LOCATOR, PRICE_LOCATOR)

    if number_of_pages > 1:
        for i in range(2, number_of_pages+1):
            wait_func()
            page.locator(PAGINATION_BUTTON).click()
            wait_func(6)
            list_of_models_and_prices = get_lists_of_smartphones_and_prices(page, MODEL_LOCATOR, PRICE_LOCATOR)

    print(f"Найдено {len(list_of_models_and_prices[0])} акционных моделей бренда Tecno в наличии")

    create_csv_file_with_chosen_models(list_of_models_and_prices)

    context.close()
    browser.close()


with sync_playwright() as playwright:
    start_scraping(playwright)