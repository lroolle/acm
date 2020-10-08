""" Configs Default for example

1. Basedir to doc your personal leetcode problems

For example:
    /path/to/leetcode(basedir)
    ├── 0003_longest-substring-without-repeating-characters
    │   ├── README.org
    │   ├── article
    │   └── solution
    ├── 0006_zigzag-conversion
    │   ├── README.org
    │   ├── article
    │   └── solution

2. Cookies.txt: For cache/load cookies to/from, persist both cn/com domain cookies.
    a). A Mozilla/Netscape format `cookies.txt`. *NOTE: You may need a Chrome Extension called: cookies.txt*
    b). If no cookies file loaded, try load from your local browser(chrome/firefox),
    by `browser_cookie3`, make sure you've logged in before requet.
    c). If cookies expires or not valid, clear and try again.
"""

# Cookies.txt(Include both leetcode-cn.com && leetcode.com )
COOKIES_FILE = "/tmp/leetcode.cookies.txt"

# Leetcode-cn.com Usernmae & Password
LEETCODE_USERNMAE_CN = ""
LEETCODE_PASSWORD_CN = ""

# Leetcode.com Usernmae & Password
# Try to login leetcode.com is awfully sick Ewww... for recaptcha's sake
LEETCODE_USERNMAE = ""
LEETCODE_PASSWORD = ""

# Preferences for doc problems
LEETCODE_BASEDIR = "~/algorigthm/leetcode"
PREFER_LANG = "go"  # Solution lang
PREFER_DOC_STYLE = "org"  # or md
