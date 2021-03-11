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
import { Octokit } from "@octokit/core"
import { sanitizeGraphQL } from "../../util/safety"
import { getConfig } from "../config"

function makeOctokit(): Octokit {
    return new Octokit({
        auth: getConfig().githubToken,
        timeZone: "America/New_York",
    })
}

const cakebotRepoMetaQuery = (owner: string, name: string) => `query {
    repository(owner: "${owner}", name: "${name}") {
        stargazerCount
        homepageUrl
    }
}`

export interface CakebotMetaQueryResponse {
    repository: {
        stargazerCount: number
        homepageUrl?: string
    }
}

export default function getRepositoryMetadata(
    repository: string
): Promise<CakebotMetaQueryResponse> {
    repository = sanitizeGraphQL(repository)

    const owner = repository.split("/")[0]
    const repoName = repository.split("/")[1]

    return new Promise<CakebotMetaQueryResponse>((resolve, reject) => {
        makeOctokit()
            .graphql(cakebotRepoMetaQuery(owner, repoName))
            .then((data) => resolve(data as CakebotMetaQueryResponse))
            .catch((e) => reject(e))
    })
}
