import pytest
from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

URL = "http://www.uitestingplayground.com/"


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def test_01_css_xpath__dynamicid(driver):
    driver.get(URL + "dynamicid")
    assert driver.find_element(By.XPATH, "//button[normalize-space()='Button with Dynamic ID']")
    assert driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")


def test_02_css_xpath__classattr(driver):
    driver.get(URL + "classattr")
    button3 = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-primary')]")
    assert button3
    assert driver.find_element(By.CSS_SELECTOR, "button.btn-primary")

    button3.click()
    alert = Alert(driver)
    assert alert.text == 'Primary button pressed'
    alert.accept()


def test_03_css_xpath__hiddenlayers(driver):
    driver.get(URL + "hiddenlayers")
    green_button_xpath = driver.find_element(By.XPATH, "//button[@id='greenButton']")
    green_button_ccs = driver.find_element(By.CSS_SELECTOR, "#greenButton")
    assert green_button_xpath.is_displayed()
    assert green_button_ccs.is_displayed()

    green_button_xpath.click()
    with pytest.raises(ElementClickInterceptedException):
        green_button_xpath.click()


def test_04_css_xpath__home_page_links(driver):
    driver.get(URL)
    all_links_xpath = driver.find_elements(By.XPATH, "//h3/a")
    all_links_ccs = driver.find_elements(By.CSS_SELECTOR, "h3 a")
    assert len(all_links_xpath) == 18
    assert len(all_links_ccs) == 18


def test_05_css_xpath__home_page_menu(driver):
    driver.get(URL)
    uitap_xpath = driver.find_element(By.XPATH, "//a[@class='navbar-brand']")
    uitap_ccs = driver.find_element(By.CSS_SELECTOR, ".navbar-brand")
    assert uitap_xpath.is_displayed()
    assert uitap_ccs.is_displayed()


def test_06_css_xpath__home_page_home(driver):
    driver.get(URL)
    home_xpath = driver.find_element(By.XPATH, "//a[@class='nav-link' and @href='/home']")
    home_ccs = driver.find_element(By.CSS_SELECTOR, ".nav-link[href='/home']")
    assert home_xpath.is_displayed()
    assert home_ccs.is_displayed()


def test_07_08_css_xpath__loaddelay(driver):
    driver.get(URL)
    loaddelay_xpath = driver.find_element(By.XPATH, "//a[@href='/loaddelay']")
    loaddelay_ccs = driver.find_element(By.CSS_SELECTOR, "a[href='/loaddelay']")

    assert loaddelay_xpath.is_displayed()
    assert loaddelay_xpath.is_displayed()

    loaddelay_ccs.click()
    button_after_delay = WebDriverWait(driver, 30).until(
        lambda x: x.find_element(By.XPATH, "//button[normalize-space()='Button Appearing After Delay']")
    )
    assert button_after_delay.is_displayed()


def test_09_10_css_xpath__ajax(driver):
    driver.get(URL)
    ajax_xpath = driver.find_element(By.XPATH, "//a[@href='/ajax']")
    ajax_ccs = driver.find_element(By.CSS_SELECTOR, "a[href='/ajax']")

    assert ajax_xpath.is_displayed()
    assert ajax_ccs.is_displayed()

    ajax_xpath.click()

    ajax_triggering_button = driver.find_element(By.XPATH, "//button[text()='Button Triggering AJAX Request']")
    ajax_triggering_button.click()

    ajax_loaded = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.XPATH, "//p[@class='bg-success' and text()='Data loaded with AJAX get request.']")
        )
    )

    assert ajax_loaded.is_displayed()
