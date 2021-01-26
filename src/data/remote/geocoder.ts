/**
 * @fileoverview Local reverse geocoder based on GeoNames data.
 * @author Thomas Steiner (tomac@google.com)
 * @license Apache 2.0
 *
 * @example
 * // With just one point
 * var point = {latitude: 42.083333, longitude: 3.1};
 * geocoder.lookUp(point, 1, function(err, res) {
 *   console.log(JSON.stringify(res, null, 2));
 * });
 */

/* eslint-disable */

import parse from "csv-parse"
import fs from "fs"
// @ts-ignore
import kdTree from "kdt"
// @ts-ignore
import unzip from "node-unzip-2"
import path from "path"
import request from "request"

// All data from https://download.geonames.org/export/dump/
const GEONAMES_URL = "https://download.geonames.org/export/dump/"

const CITIES_FILE = "cities1000"

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

const GEONAMES_DUMP = __dirname + "/geonames_dump"
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
// http://www.movable-type.co.uk/scripts/latlong.html
export function distanceFunc(x: NumberPoint, y: NumberPoint) {
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

function _getGeoNamesCitiesData(callback: any): void {
    const now = new Date().toISOString().substr(0, 10)
    // Use timestamped cities file OR bare cities file
    const timestampedFilename =
        GEONAMES_DUMP + "/cities/" + CITIES_FILE + "_" + now + ".txt"
    if (fs.existsSync(timestampedFilename)) {
        return callback(timestampedFilename)
    }

    const filename = GEONAMES_DUMP + "/cities/" + CITIES_FILE + ".txt"
    if (fs.existsSync(filename)) {
        return callback(filename)
    }
    const options = {
        url: GEONAMES_URL + CITIES_FILE + ".zip",
        encoding: null,
    }
    request.get(
        options,
        function (
            err: Error | undefined,
            response: { statusCode: number },
            body: string
        ) {
            if (err || response.statusCode !== 200) {
                return callback(
                    "Error downloading GeoNames cities data" +
                        (err ? ": " + err : "")
                )
            }
            // Store a dump locally
            if (!fs.existsSync(GEONAMES_DUMP + "/cities")) {
                fs.mkdirSync(GEONAMES_DUMP + "/cities")
            }
            const zipFilename =
                GEONAMES_DUMP + "/cities/" + CITIES_FILE + "_" + now + ".zip"
            try {
                fs.writeFileSync(zipFilename, body)
                fs.createReadStream(zipFilename)
                    .pipe(unzip.Extract({ path: GEONAMES_DUMP + "/cities" }))
                    .on("close", function () {
                        fs.renameSync(filename, timestampedFilename)
                        fs.unlinkSync(
                            GEONAMES_DUMP +
                                "/cities/" +
                                CITIES_FILE +
                                "_" +
                                now +
                                ".zip"
                        )
                        // Housekeeping, remove old files
                        const currentFileName = path.basename(
                            timestampedFilename
                        )
                        fs.readdirSync(GEONAMES_DUMP + "/cities").forEach(
                            function (file) {
                                if (file !== currentFileName) {
                                    fs.unlinkSync(
                                        GEONAMES_DUMP + "/cities/" + file
                                    )
                                }
                            }
                        )
                        return callback(timestampedFilename)
                    })
            } catch (e) {
                return callback(timestampedFilename)
            }
        }
    )
}

function _parseGeoNamesCitiesCsv(pathToCsv: string, callback: any): void {
    const data: unknown[] = []
    const content = fs.readFileSync(pathToCsv)
    parse(content, { delimiter: "\t", quote: "" }, (err, lines) => {
        if (err) {
            return callback(err)
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
        return callback()
    })
}

export function init(): void {
    // Create local cache folder
    if (!fs.existsSync(GEONAMES_DUMP)) {
        fs.mkdirSync(GEONAMES_DUMP)
    }
    _getGeoNamesCitiesData((e: string) => _parseGeoNamesCitiesCsv(e, () => {}))
}

export function lookUp(
    point: StringPoint,
    callback: (result: LookupResult) => void
): void {
    if (!theKdTree) {
        // todo
    }
    const p = {
        latitude: parseFloat(point.latitude),
        longitude: parseFloat(point.longitude),
    }
    // @ts-ignore
    const result = theKdTree.nearest(p, 1)
    result.reverse()
    for (let j = 0, lenJ = result.length; j < lenJ; j++) {
        if (result && result[j] && result[j][0]) {
            // Simplify the output by not returning an array
            result[j] = result[j][0]
        }
    }
    return callback(result)
}
