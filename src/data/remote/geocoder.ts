/**
 * @fileoverview Local reverse geocoder based on GeoNames data.
 * @author Thomas Steiner (tomac@google.com)
 * @license Apache 2.0
 *
 * @param {(object|object[])} points One single or an array of
 *                                   latitude/longitude pairs
 * @callback callback The callback function with the results
 *
 * @returns {object[]} An array of GeoNames-based geocode results
 *
 * @example
 * // With just one point
 * var point = {latitude: 42.083333, longitude: 3.1};
 * geocoder.lookUp(point, 1, function(err, res) {
 *   console.log(JSON.stringify(res, null, 2));
 * });
 *
 * // In batch mode with many points
 * var points = [
 *   {latitude: 42.083333, longitude: 3.1},
 *   {latitude: 48.466667, longitude: 9.133333}
 * ];
 * geocoder.lookUp(points, 1, function(err, res) {
 *   console.log(JSON.stringify(res, null, 2));
 * });
 */

/* eslint-disable */

import async from "async"
import parse from "csv-parse"
import fs from "fs"
// @ts-ignore
import kdTree from "kdt"
// @ts-ignore
import unzip from "node-unzip-2"
import path from "path"
import request from "request"

// All data from http://download.geonames.org/export/dump/
const GEONAMES_URL = "http://download.geonames.org/export/dump/"

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

let GEONAMES_DUMP = __dirname + "/geonames_dump"

class Geocoder {
    private _kdTree?: unknown

    // Distance function taken from
    // http://www.movable-type.co.uk/scripts/latlong.html
    public static _distanceFunc(x: any, y: any) {
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

    private _getGeoNamesCitiesData(callback: any) {
        const now = new Date().toISOString().substr(0, 10)
        // Use timestamped cities file OR bare cities file
        const timestampedFilename =
            GEONAMES_DUMP + "/cities/" + CITIES_FILE + "_" + now + ".txt"
        if (fs.existsSync(timestampedFilename)) {
            return callback(null, timestampedFilename)
        }

        const filename = GEONAMES_DUMP + "/cities/" + CITIES_FILE + ".txt"
        if (fs.existsSync(filename)) {
            return callback(null, filename)
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
                    GEONAMES_DUMP +
                    "/cities/" +
                    CITIES_FILE +
                    "_" +
                    now +
                    ".zip"
                try {
                    fs.writeFileSync(zipFilename, body)
                    fs.createReadStream(zipFilename)
                        .pipe(
                            unzip.Extract({ path: GEONAMES_DUMP + "/cities" })
                        )
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
                            return callback(null, timestampedFilename)
                        })
                } catch (e) {
                    return callback(null, timestampedFilename)
                }
            }
        )
    }

    private _parseGeoNamesCitiesCsv(pathToCsv: string, callback: any) {
        const data: {}[] = []
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
            this._kdTree = kdTree.createKdTree(
                data,
                Geocoder._distanceFunc,
                dimensions
            )
            return callback()
        })
    }

    public init(options: any) {
        options = options || {}
        if (options.dumpDirectory) {
            GEONAMES_DUMP = options.dumpDirectory
        }

        // Create local cache folder
        if (!fs.existsSync(GEONAMES_DUMP)) {
            fs.mkdirSync(GEONAMES_DUMP)
        }
        async.waterfall([
            this._getGeoNamesCitiesData.bind(this),
            this._parseGeoNamesCitiesCsv.bind(this),
        ])
    }

    public lookUp(point: any, callback: any) {
        // @ts-ignore
        this._lookUp(point, function (err?: Error, results: any) {
            return callback(null, results)
        })
    }

    private _lookUp(point: any, callback: any) {
        if (!this._kdTree) {
            // todo
        }
        const p = {
            latitude: parseFloat(point.latitude),
            longitude: parseFloat(point.longitude),
        }
        // @ts-ignore
        const result = this._kdTree.nearest(p, 1)
        result.reverse()
        for (let j = 0, lenJ = result.length; j < lenJ; j++) {
            if (result && result[j] && result[j][0]) {
                // Simplify the output by not returning an array
                result[j] = result[j][0]
            }
        }
        return callback(result)
    }
}

export default Geocoder
