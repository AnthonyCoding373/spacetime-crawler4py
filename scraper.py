import re
from urllib.parse import urlparse

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    found_urls = set()

    if resp.status == 200:
        try:
            content_string = resp.raw_response.content.decode("utf-8", errors="ignore")


        except Exception as e:
            return []

        attr_pattern = r'(?:href|src)\s*=\s*["\']([^"\']+)["\']'
        attribute_urls = re.findall(attr_pattern, content_string, re.IGNORECASE)

        for href in attribute_urls:
            href = href.strip()

            if href and not href.startswith("#"):
                found_urls.add(href)

    return list(found_urls)

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in {'http', 'https'}:
            return False
        hostname = parsed.hostname
        if not hostname:
            return False
        if '/wp-json/' in url:
            return False
        #Might not be necessary to have
        if '?share=' in url:
            return False
        hostname = hostname.lower()
        hostname_parts = hostname.split('.')
        required_parts = ['ics', 'uci', 'edu']
        if len(hostname_parts) < len(required_parts):
            return False
        if hostname_parts[-len(required_parts):] != required_parts:
            return False
        if 'date=' in url or 'date=' in url or 'day' in url or 'events' in url or 'event' in url:
            return False 
        #for path for disallowed file extensions
        path = parsed.path.lower()
        if re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico|png|tiff?|mid|mp2|mp3|mp4"
            r"|wav|ppsx|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf|ps|eps|tex|ppt|pptx"
            r"|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd"
            r"|dmg|iso|epub|dll|cnf|tgz|sha1|thmx|mso|arff|rtf|jar|csv|rm"
            r"|smil|wmv|swf|wma|zip|rar|gz)$", path):
            return False
        # to avoid URLs with certain query parameters (traps)
        query = parsed.query.lower()
        if any(param in query for param in ['sid=', 'session_id=', 'sessionid=', 'user=']):
            return False
        return True
    except TypeError:
        print ("TypeError for ", parsed)
        raise

