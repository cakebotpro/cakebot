/* eslint-disable */

/**
 * This is a launcher implementation meant for development purposes,
 * but you can also use it in production if you don't need to register any extra
 * features to the bot.
 */

const start = require("./build/index").start
const defaultCommandsHookup = require("./build/commands/commands")
    .defaultCommandsHookup

// start with a hookup that applies the default commands
start([defaultCommandsHookup])
