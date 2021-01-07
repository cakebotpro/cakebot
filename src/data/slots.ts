/**
 * Cakebot - A fun and helpful Discord bot
 * Copyright (C) 2021-current year  Reece Dunham
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

import random from "random"

/**
 * All the possible emojis.
 */
export const emojis = ["🍎", "🍊", "🍐", "🍋", "🍉", "🍇", "🍒"]

/**
 * This is a special character. It is *not* a space, but instead
 * the braille character with no dots raised (effectively making
 * it bypass Discord's trimmer for spaces before the actual message
 * being sent.)
 */
export const BRAILLE_ZERO_DOT_CHAR = "⠀"

interface SlotRoll {
    row1: string
    row2: string
    row3: string
    winningRoll: boolean
    displayTip: boolean
}

/**
 * Get a random emoji.
 */
const getEmoji = () => emojis[random.int(0, emojis.length - 1)]

/**
 * Roll a slots game.
 */
export default function roll(): SlotRoll {
    // todo: allow this to be configured
    const WIN_CHANCE = 50

    const win: boolean = random.int(0, WIN_CHANCE) === 20

    return {
        winningRoll: win,
        displayTip: random.int(0, 20) === 15,
        row1: `${BRAILLE_ZERO_DOT_CHAR}${BRAILLE_ZERO_DOT_CHAR} ${getEmoji()}${getEmoji()}${getEmoji()}`,
        row2: `:arrow_forward: ${getEmoji()}${getEmoji()}${getEmoji()} :arrow_backward:`,
        row3: `${BRAILLE_ZERO_DOT_CHAR}${BRAILLE_ZERO_DOT_CHAR} ${getEmoji()}${getEmoji()}${getEmoji()}\n\n${
            win ? "**You win!**" : "You Lose. Better luck next time."
        }`,
    }
}
