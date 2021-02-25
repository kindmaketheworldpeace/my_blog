/**
 * @file config
 * @author ielgnaw <wuji0223@gmail.com>
 */

import path from 'path'
import prodEnv from './prod.env'
import devEnv from './dev.env'

// 打包的目标，cd ci all
const BUILD_TARGET = process.argv[3]

export default {
    build: {
        env: prodEnv,
        assetsRoot: path.resolve(__dirname, '../../static'),
        assetsSubDirectory: 'assets/',
        assetsPublicPath: '../../',
        productionSourceMap: true,
        productionGzip: false,
        productionGzipExtensions: ['js', 'css'],
        bundleAnalyzerReport: process.env.npm_config_report
    },

    dev: {
        env: devEnv,
        port: 8002,
        assetsSubDirectory: 'static',
        assetsPublicPath: '/',
        proxyTable: {},
        cssSourceMap: false,
        autoOpenBrowser: true
    }
}
