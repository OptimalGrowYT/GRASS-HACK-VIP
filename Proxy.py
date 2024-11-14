import requests

# Read proxies from proxy.txt file
def read_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = file.readlines()
    # Clean up any extra whitespace characters like \n
    return [proxy.strip() for proxy in proxies]

# Sample URL to test the proxies
test_url = "http://httpbin.org/ip"

# Function to test proxies
def test_proxy(proxy):
    try:
        response = requests.get(test_url, proxies={"socks5": proxy}, timeout=5)
        if response.status_code == 200:
            print(f"Working: {proxy}")
        else:
            print(f"Failed: {proxy}")
    except requests.exceptions.RequestException as e:
        print(f"Error with {proxy}: {e}")

# Main function
def main():
    proxy_file = "proxy.txt"  # Path to the proxy list file
    proxies = read_proxies(proxy_file)

    # Loop through all proxies and test them
    for proxy in proxies:
        test_proxy(proxy)

if __name__ == "__main__":
    main()
