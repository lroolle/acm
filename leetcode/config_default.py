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

2. Cookies.txt: For save/load cookies to/from, persist both cn/com domain cookies.
    a). Recommend Format: A Mozilla/Netscape `cookies.txt` format.
        *You may need a Chrome Extension called: cookies.txt*

    b). Manually Copy/Paste Format: copied from chrome headers
        For example, "chips=ahoy; vienna=finger"

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
