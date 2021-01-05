import logger from "../util/logging"

export interface Configuration {
    discordToken: string
    wordsapiToken?: string
    githubToken?: string
}

interface ExpectedEnvironment {
    DISCORD_TOKEN: string
    WORDSAPI_TOKEN?: string
    GITHUB_TOKEN?: string
}

export function getConfig(): Configuration {
    const env = (process.env as unknown) as ExpectedEnvironment

    const config = {
        discordToken: env.DISCORD_TOKEN,
        wordsapiToken: env.GITHUB_TOKEN,
        githubToken: env.GITHUB_TOKEN,
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
