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
import { getConfig } from "../config"
import { asyncGetAndConsume } from "./runtime-downloads"

export interface DefineResult {
    defs: string[]
    syllables: string
}

interface SyllablesCast {
    list: string[]
}

interface DefResultCast {
    results: {
        definition: string
        partOfSpeech: string
    }[]
}

export default function define(word: string): Promise<DefineResult> {
    return new Promise((resolve, reject) => {
        try {
            asyncGetAndConsume(
                `https://wordsapiv1.p.rapidapi.com/words/${word}`,
                function consumeWordFetch(data) {
                    const syllables =
                        ((data.syllables as unknown) as SyllablesCast)?.list ||
                        []
                    const defResults: string[] = ((data as unknown) as DefResultCast).results.map(
                        (result) =>
                            `${result.partOfSpeech}: ${result.definition}`
                    )

                    const returnResult: DefineResult = {
                        syllables: syllables.join(", "),
                        defs: defResults,
                    }

                    resolve(returnResult)
                },
                {
                    headers: {
                        "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
                        "x-rapidapi-key": (getConfig()
                            .wordsapiToken as unknown) as never,
                    },
                }
            )
        } catch (e) {
            reject(e)
        }
    })
}
