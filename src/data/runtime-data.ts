import download from "./runtime-downloads"

export const eightballs = download(
    "https://raw.githubusercontent.com/cakebotpro/cakebot/master/content/8ball.txt"
)

export const jokes = download(
    "https://raw.githubusercontent.com/cakebotpro/cakebot/master/content/jokes.txt"
)
