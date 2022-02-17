from selenium import webdriver


def main():
    driver = webdriver.Safari()
    driver.get('https://vk.com/')

    element = driver.find_element()

    print(element)


if __name__ == "__main__":
    main()
