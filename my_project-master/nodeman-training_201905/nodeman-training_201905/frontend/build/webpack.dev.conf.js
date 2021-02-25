/**
 * @file webpack dev config
 * @author ielgnaw <wuji0223@gmail.com>
 */

import webpack from 'webpack'
import {join} from 'path'
import merge from 'webpack-merge'
import HtmlWebpackPlugin from 'html-webpack-plugin'
import FriendlyErrorsPlugin from 'friendly-errors-webpack-plugin'

import config from './config'
import {styleLoaders} from './util'
import baseWebpackConfig from './webpack.base.conf'

const webpackConfig = merge(baseWebpackConfig, {
    entry: {
        main: './src/main.js'
        // cd: './src/cd.js',
        // ci: './src/ci.js'
        // all: ['./build/dev-client', './src/cd.js']
    },
    module: {
        rules: styleLoaders({sourceMap: config.dev.cssSourceMap})
    },
    devtool: '#cheap-module-eval-source-map',
    plugins: [
        new webpack.DefinePlugin(config.dev.env),
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NoEmitOnErrorsPlugin(),
        new HtmlWebpackPlugin({
            filename: 'index.html',
            template: 'index.html',
            inject: true
        }),
        new FriendlyErrorsPlugin()
        // new webpack.optimize.CommonsChunkPlugin({
        //     name: 'common'
        // })
    ]
})

Object.keys(webpackConfig.entry).forEach(function(name) {
    webpackConfig.entry[name] = ['./build/dev-client'].concat(webpackConfig.entry[name])
})

export default webpackConfig
