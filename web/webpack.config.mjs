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

/* eslint-disable */

import path from "path"
import WebpackBar from "webpackbar"
import HtmlWebpackPlugin from "html-webpack-plugin"
import TerserPlugin from "terser-webpack-plugin"
import MiniCssExtractPlugin from "mini-css-extract-plugin"
import OptimizeCssAssetsPlugin from "optimize-css-assets-webpack-plugin"

process.env.NODE_ENV = "production"
process.env.BABEL_ENV = "production"

const config = {
    module: {
        strictExportPresence: true,
        rules: [
            {
                test: /\.(js|mjs|cjs|jsx|ts|tsx)$/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: [
                            [
                                "@babel/preset-env",
                                {
                                    targets: "defaults",
                                    exclude: ["transform-typeof-symbol"],
                                },
                            ],
                            "@babel/preset-react",
                            "@babel/preset-typescript",
                        ],
                        plugins: [
                            [
                                require("babel-plugin-transform-react-remove-prop-types")
                                    .default,
                                {
                                    removeImport: true,
                                },
                            ],
                        ],
                        cacheDirectory: true,
                    },
                },
            },
            {
                test: /\.css$/i,
                use: [MiniCssExtractPlugin.loader, "css-loader"],
            },
        ],
    },
    entry: path.resolve(__dirname, "src/index.tsx"),
    output: {
        path: path.join(process.cwd(), `build${path.sep}web-dist`),
        filename: "webpack.bundle.js",
        globalObject: "this",
    },
    plugins: [
        new WebpackBar({ name: "Web UI" }),
        new HtmlWebpackPlugin({
            title: "Cakebot Dashboard",
        }),
        new MiniCssExtractPlugin({
            linkType: "text/css",
        }),
        new OptimizeCssAssetsPlugin({
            cssProcessor: require("cssnano"),
            cssProcessorPluginOptions: {
                preset: ["default", { discardComments: { removeAll: true } }],
            },
            canPrint: true,
        }),
    ],
    optimization: {
        minimize: true,
        minimizer: [
            new TerserPlugin({
                terserOptions: {
                    parse: {
                        ecma: 8,
                    },
                    compress: {
                        ecma: 5,
                        warnings: false,
                        comparisons: false,
                        inline: 2,
                    },
                    mangle: {
                        safari10: true,
                    },
                    keep_classnames: true,
                    keep_fnames: true,
                    output: {
                        ecma: 5,
                        comments: false,
                        ascii_only: true,
                    },
                },
                sourceMap: true,
            }),
        ],
        splitChunks: {
            chunks: "all",
            name: true,
        },
        runtimeChunk: {
            name: entrypoint => `runtime-${entrypoint.name}`,
        },
    },
    resolve: {
        modules: ["node_modules", `${process.cwd()}/node_modules`],
        extensions: [
            ".js",
            ".web.js",
            ".jsx",
            ".web.jsx",
            "ts",
            ".web.ts",
            ".tsx",
            ".web.tsx",
            ".mjs",
            ".web.mjs",
        ],
        alias: {
            "react-dom$": "react-dom/profiling",
            "scheduler/tracing": "scheduler/tracing-profiling",
        },
    },
}

module.exports = config
