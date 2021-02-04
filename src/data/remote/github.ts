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

const repoStarsQuery = (owner: string, name: string) => `query {
    repository(owner: "${owner}", name: "${name}") {
        stargazerCount
    }
}`

const repoHomepageQuery = (owner: string, name: string) => `query {
    repository(owner: "${owner}", name: "${name}") {        
        homepageUrl
    }
}`

interface RepoStarQueryResponse {
    repository: {
        stargazerCount: number
    }
}

interface RepoHomepageQueryResponse {
    repository: {
        homepageUrl?: string
    }
}

export function getRepositoryStars(repository: string): Promise<number> {
    repository = sanitizeGraphQL(repository)

    const owner = repository.split("/")[0]
    const repoName = repository.split("/")[1]

    return new Promise<number>((resolve, reject) => {
        makeOctokit()
            .graphql(repoStarsQuery(owner, repoName))
            .then((data) =>
                resolve(
                    (data as RepoStarQueryResponse).repository.stargazerCount
                )
            )
            .catch((e) => reject(e))
    })
}

export function getRepositoryHomepage(
    repository: string
): Promise<string | undefined> {
    repository = sanitizeGraphQL(repository)

    const owner = repository.split("/")[0]
    const repoName = repository.split("/")[1]

    return new Promise<string | undefined>((resolve, reject) => {
        makeOctokit()
            .graphql(repoHomepageQuery(owner, repoName))
            .then((data) =>
                resolve(
                    (data as RepoHomepageQueryResponse).repository.homepageUrl
                )
            )
            .catch((e) => reject(e))
    })
}
