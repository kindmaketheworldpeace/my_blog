/**
 * @file dev server
 * @author ielgnaw <wuji0223@gmail.com>
 */

import express from 'express'
import path from 'path'
import webpack from 'webpack'
import bodyParser from 'body-parser'
import opn from 'opn'
import proxyMiddleware from 'http-proxy-middleware'
import webpackHotMiddleware from 'webpack-hot-middleware'
import webpackDevMiddleware from 'webpack-dev-middleware'
import history from 'connect-history-api-fallback'

import ajaxMiddleware from './ajax-middleware'
import checkVer from './check-versions'
import config from './config'
import devConf from './webpack.dev.conf'
import {getIP} from './util'

checkVer()

if (!process.env.NODE_ENV) {
    process.env.NODE_ENV = JSON.parse(config.dev.env.NODE_ENV)
}

const webpackConfig = devConf

const port = process.env.PORT || config.dev.port

const autoOpenBrowser = !!config.dev.autoOpenBrowser

const proxyTable = config.dev.proxyTable

const app = express()
const compiler = webpack(webpackConfig)

const devMiddleware = webpackDevMiddleware(compiler, {
    publicPath: webpackConfig.output.publicPath,
    quiet: true
})

const hotMiddleware = webpackHotMiddleware(compiler, {
    log: false,
    heartbeat: 2000
})

compiler.plugin('compilation', compilation => {
    compilation.plugin('html-webpack-plugin-after-emit', (data, cb) => {
        hotMiddleware.publish({action: 'reload'})
        cb()
    })
})

Object.keys(proxyTable).forEach(context => {
    let options = proxyTable[context]
    if (typeof options === 'string') {
        options = {
            target: options
        }
    }
    app.use(proxyMiddleware(context, options))
})

app.use(history({
    verbose: true,
    rewrites: [
        {
            // connect-history-api-fallback 默认会对 url 中有 . 的 url 当成静态资源处理而不是当成页面地址来处理
            // 兼容 /cs/28aa9eda67644a6eb254d694d944307e/cluster/BCS-MESOS-10001/node/10.121.23.12 这样以 IP 结尾的 url
            // from: /\d+\.\d+\.\d+\.\d+$/,
            from: /(\d+\.)*\d+$/,
            to: '/'
        },
        {
            // connect-history-api-fallback 默认会对 url 中有 . 的 url 当成静态资源处理而不是当成页面地址来处理
            // 兼容 /bcs/projectId/app/214/taskgroups/0.application-1-13.test123.10013.1510806131114508229/containers/containerId
            from: /\/+.*\..*\//,
            to: '/'
        }
    ]
}))

app.use(devMiddleware)

app.use(hotMiddleware)

app.use(bodyParser.json())

app.use(bodyParser.urlencoded({
    extended: true
}))

app.use(ajaxMiddleware)

const staticPath = path.posix.join(config.dev.assetsPublicPath, config.dev.assetsSubDirectory)
app.use(staticPath, express.static('./static'))

const url = `http://nodeman-dev.open.oa.com:${port}`

let _resolve
const readyPromise = new Promise(resolve => {
    _resolve = resolve
})

console.log('> Starting dev server...')
devMiddleware.waitUntilValid(() => {
    console.log('> Listening at ' + url + '\n')
    console.log('Other available url: ')
    console.log(`http://${getIP()}:${port}`)
    console.log(`http://localhost:${port}\n`)
    if (autoOpenBrowser) {
        opn(url)
    }
    _resolve()
})

const server = app.listen(port)

export default {
    ready: readyPromise,
    close: () => {
        server.close()
    }
}
