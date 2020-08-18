import urllib.request
import json


def kakusu(character):
    # convert character to he x unicode
    letter_a = str(character)
    decimal_a = ord(letter_a)
    hex_A = hex(decimal_a)

    # insert into api request format
    request_url = "https://mojikiban.ipa.go.jp/mji/q?UCS=*"
    request_url = request_url.replace('*', hex_A)

    req = urllib.request.Request(request_url)

    with urllib.request.urlopen(req) as res:
        body = json.load(res)

    return body['results'][0]["総画数"]


if __name__ == "__main__":
    setntence = "福島県会津若松市一箕町大字鶴賀字上居合会津大学創明寮号室"
    cnt = 0
    for letter in setntence:
        cnt += kakusu(letter)
    print(cnt)
