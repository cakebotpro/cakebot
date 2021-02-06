/**
 * @fileoverview Local reverse geocoder based on GeoNames data.
 * @author Thomas Steiner (tomac@google.com)
 * @license Apache 2.0
 */

/* eslint-disable header/header */

import parse from "csv-parse"
import { readFileSync } from "fs"
// @ts-ignore
import kdTree from "kdt"
import { CONTENT_FOLDER } from "./runtime-data"
import { sep } from "path"

const CITIES_FILE = `${CONTENT_FOLDER}${sep}geocoder-cities-data.txt`

const GEONAMES_COLUMNS = [
    "geoNameId",
    "name",
    "asciiName",
    "alternateNames",
    "latitude",
    "longitude",
    "featureClass",
    "featureCode",
    "countryCode",
    "cc2",
    "admin1Code",
    "admin2Code",
    "admin3Code",
    "admin4Code",
    "population",
    "elevation",
    "dem",
    "timezone",
    "modificationDate",
]

let theKdTree: unknown = undefined

export interface StringPoint {
    latitude: string
    longitude: string
}

export interface NumberPoint {
    latitude: number
    longitude: number
}

export interface LookupResult {
    name: string
    countryCode: string
}

// Distance function taken from
// https://www.movable-type.co.uk/scripts/latlong.html
export function distanceFunc(x: NumberPoint, y: NumberPoint): number {
    function toRadians(num: number): number {
        return (num * Math.PI) / 180
    }

    const lat1 = x.latitude
    const lon1 = x.longitude
    const lat2 = y.latitude
    const lon2 = y.longitude

    const R = 6371 // km
    const o1 = toRadians(lat1)
    const o2 = toRadians(lat2)
    const to = toRadians(lat2 - lat1)
    const tl = toRadians(lon2 - lon1)
    const a =
        Math.sin(to / 2) * Math.sin(to / 2) +
        Math.cos(o1) * Math.cos(o2) * Math.sin(tl / 2) * Math.sin(tl / 2)
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
    return R * c
}

export function init(): void {
    const data: unknown[] = []
    const content = readFileSync(CITIES_FILE)
    parse(
        content,
        { delimiter: "\t", quote: "" },
        function cbCsvParseCallback(err, lines): void {
            if (err) {
                throw err
            }
            lines.forEach(function (line: string) {
                const lineObj = {}
                for (let i = 0; i < GEONAMES_COLUMNS.length; i++) {
                    // @ts-ignore
                    lineObj[GEONAMES_COLUMNS[i]] = line[i] || null
                }
                data.push(lineObj)
            })

            const dimensions = ["latitude", "longitude"]
            theKdTree = kdTree.createKdTree(data, distanceFunc, dimensions)
        }
    )
}

export function lookUp(point: StringPoint): LookupResult | null {
    if (!theKdTree) {
        return null
    }

    const p = {
        latitude: parseFloat(point.latitude),
        longitude: parseFloat(point.longitude),
    }

    // @ts-ignore
    let result = theKdTree.nearest(p, 1)
    result.reverse()

    for (let j = 0, lenJ = result.length; j < lenJ; j++) {
        if (result && result[j] && result[j][0]) {
            // Simplify the output by not returning an array
            result = result[j][0]
        }
    }

    return result
}
