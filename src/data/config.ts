import logger from "../util/logging"

export interface Configuration {
    discordToken: string
    wordsapiToken?: string
    githubToken?: string
    debug: boolean
}

interface ExpectedEnvironment {
    DISCORD_TOKEN: string
    WORDSAPI_TOKEN?: string
    GITHUB_TOKEN?: string
    DEBUG?: string
}

function isTruthish(v?: string): boolean {
    if (!v) {
        return false
    }

    return v.toLowerCase() === "true"
}

export function getConfig(): Configuration {
    const env = (process.env as unknown) as ExpectedEnvironment

    const config = {
        discordToken: env.DISCORD_TOKEN,
        wordsapiToken: env.GITHUB_TOKEN,
        githubToken: env.GITHUB_TOKEN,
        debug: isTruthish(env.DEBUG),
    }

    if (validateConfig(config)) {
        return config
    }

    logger.error(
        `No Discord token specified! You need to put it in the .env file, with the variable being called 'DISCORD_TOKEN'!`
    )
    process.exit(1)
}

function validateConfig(config: Configuration): boolean {
    return !!config.discordToken
}
