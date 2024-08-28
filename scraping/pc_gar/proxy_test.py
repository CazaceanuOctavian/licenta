from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType

options = Options()

my_proxy = '91.107.252.136:80'

options.proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    "socksVersion": 4,
    'httpProxy': my_proxy,    
    'sslProxy': my_proxy,
    "socksProxy": my_proxy,
    'noProxy':''})

#options.add_argument(f'--proxy-server={PROXY}')
options.binary_location = '/etc/firefox'
# options.set_preference('network.proxy.type', 1)
# options.set_preference('network.proxy.socks', '152.26.229.86')
# options.set_preference('network.proxy.socks_port', 9443)
# options.set_preference('network.proxy.socks_remote_dns', True)
driver = webdriver.Firefox(options=options)

driver.get('https://www.pcgarage.ro/cabluri-date/pagina13/')
pagesource = driver.page_source
print(pagesource)