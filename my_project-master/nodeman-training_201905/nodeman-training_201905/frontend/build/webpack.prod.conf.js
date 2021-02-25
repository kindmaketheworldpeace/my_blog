/**
 * @file webpack prod config
 * @author ielgnaw <wuji0223@gmail.com>
 */

import {resolve, join, sep} from 'path'
import webpack from 'webpack'
import merge from 'webpack-merge'
import CopyWebpackPlugin from 'copy-webpack-plugin'
import HtmlWebpackPlugin from 'html-webpack-plugin'
import ExtractTextPlugin from 'extract-text-webpack-plugin'
import OptimizeCSSPlugin from 'optimize-css-assets-webpack-plugin'
import CompressionWebpackPlugin from 'compression-webpack-plugin'
import bundleAnalyzer from 'webpack-bundle-analyzer'
import UglifyJsPlugin from 'uglifyjs-webpack-plugin'
import LodashModuleReplacementPlugin from 'lodash-webpack-plugin'

import config from './config'
import baseWebpackConfig from './webpack.base.conf'
import {styleLoaders, assetsPath} from './util'

const webpackConfig = merge(baseWebpackConfig, {
    entry: {
        ['app']: './src/main.js'
    },
    module: {
        rules: styleLoaders({
            sourceMap: config.build.productionSourceMap,
            extract: true
        })
    },
    devtool: config.build.productionSourceMap ? '#source-map' : false,
    output: {
        path: config.build.assetsRoot,
        filename: assetsPath('js/[name].js'),
        chunkFilename: assetsPath('js/[name].js')
    },
    plugins: [
        new webpack.DefinePlugin(config.build.env),

        new UglifyJsPlugin({
            uglifyOptions: {
                compress: {
                    warnings: false
                }
            },
            parallel: true,
            sourceMap: true
        }),

        new LodashModuleReplacementPlugin,

        new ExtractTextPlugin({
            filename: assetsPath('css/[name].css')
        }),

        new OptimizeCSSPlugin({
            cssProcessorOptions: {
                safe: true
            }
        }),

        new HtmlWebpackPlugin({
            // filename: config.build.assetsRoot + sep + config.build.assetsSubDirectory + '/index.html',
            filename: resolve(config.build.assetsRoot + sep + config.build.assetsSubDirectory, '..') + '/index.html',
            template: 'index.html',
            inject: true,
            minify: {
                removeComments: false,
                collapseWhitespace: false,
                removeAttributeQuotes: false
            },
            // 如果打开 vendor 和 manifest 那么需要配置 chunksSortMode 保证引入 script 的顺序
            chunksSortMode: 'dependency'
        }),
        new webpack.HashedModuleIdsPlugin(),
        new webpack.optimize.CommonsChunkPlugin({
            name: 'vendor',
            minChunks: ({resource}) => (
                resource
                    && resource.indexOf('node_modules') >= 0
                    && resource.match(/\.js$/)
            )
        }),
        new webpack.optimize.CommonsChunkPlugin({
            async: 'common-lazy',
            minChunks: ({resource} = {}) => (
                resource
                    && resource.includes('node_modules')
                    && /bkc/.test(resource)
                    && /bkc-ui/.test(resource)
            )
        }),
        new webpack.optimize.CommonsChunkPlugin({
            async: 'twice',
            minChunks: (module, count) => (count >= 2)
        }),
        new CopyWebpackPlugin([
            {
                from: resolve(__dirname, '../static'),
                to: config.build.assetsSubDirectory,
                ignore: ['.*']
            }
        ])
        // new AdjustScriptTagPlugin({options: ''})
    ]
})

if (config.build.productionGzip) {
    webpackConfig.plugins.push(
        new CompressionWebpackPlugin({
            asset: '[path].gz[query]',
            algorithm: 'gzip',
            test: new RegExp('\\.(' + config.build.productionGzipExtensions.join('|') +')$'),
            threshold: 10240,
            minRatio: 0.8
        })
    )
}

if (config.build.bundleAnalyzerReport) {
    const BundleAnalyzerPlugin = bundleAnalyzer.BundleAnalyzerPlugin
    webpackConfig.plugins.push(new BundleAnalyzerPlugin())
}

export default webpackConfig
