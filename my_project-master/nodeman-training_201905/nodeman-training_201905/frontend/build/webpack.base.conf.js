/**
 * @file webpack base config
 * @author ielgnaw <wuji0223@gmail.com>
 */

import path from 'path'
import webpack from 'webpack'
import friendlyFormatter from 'eslint-friendly-formatter'

import config from './config'
import {assetsPath, cssLoaders} from './util'
import {strip, fetch} from './strip-tags'

function resolve(dir) {
    return path.join(__dirname, '..', dir)
}

const isProd = process.env.NODE_ENV === 'production'

export default {
    output: {
        path: config.build.assetsRoot,
        filename: '[name].js',
        publicPath: isProd ? config.build.assetsPublicPath : config.dev.assetsPublicPath
    },
    resolve: {
        extensions: ['.js', '.vue', '.json'],
        alias: {
            'vue': 'vue/dist/vue.esm.js',
            '@': resolve('src'),
            'jquery': 'jquery/dist/jquery.min.js',
            'echarts$': 'echarts/dist/echarts.min.js',
            'echarts': 'echarts',
            'zrender$': 'zrender/dist/zrender.min.js',
            'zrender': 'zrender'
        }
    },
    cache: true,
    plugins: [
        // 域名提升
        new webpack.optimize.ModuleConcatenationPlugin(),
        // moment 优化，只提取本地包
        new webpack.ContextReplacementPlugin(/moment\/locale$/, /zh-cn/),
        // brace 优化，只提取需要的语法
        new webpack.ContextReplacementPlugin(/brace\/mode$/, /^\.\/(json|python|sh|text)$/),
        // brace 优化，只提取需要的 theme
        new webpack.ContextReplacementPlugin(/brace\/theme$/, /^\.\/(monokai)$/)
    ],
    module: {
        // for es5 file
        noParse: [
            /\/node_modules\/jquery\/dist\/jquery\.min\.js$/,
            /\/node_modules\/echarts\/dist\/echarts\.min\.js$/
        ],
        rules: [
            {
                test: /\.(js|vue)$/,
                loader: 'eslint-loader',
                enforce: 'pre',
                include: [resolve('src'), resolve('test'), resolve('static')],
                exclude: /node_modules/,
                options: {
                    formatter: friendlyFormatter
                }
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader',
                options: {
                    loaders: cssLoaders({
                        sourceMap: isProd ? config.build.productionSourceMap : config.dev.cssSourceMap,
                        extract: isProd
                    }),
                    transformToRequire: {
                        video: 'src',
                        source: 'src',
                        img: 'src',
                        image: 'xlink:href'
                    }
                }
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                include: [resolve('src'), resolve('node_modules/@tencent/bkc'), resolve('node_modules/vue-echarts')],
                // exclude (modulePath) {
                //     console.log(modulePath)
                // },
                query: {
                    cacheDirectory: './webpack_cache/'
                }
            },
            {
                test: /\.(png|jpe?g|gif|svg)(\?.*)?$/,
                loader: 'url-loader',
                options: {
                    limit: 15000,
                    name: assetsPath('img/[name].[hash:7].[ext]')
                }
            },
            {
                test: /\.(mp4|webm|ogg|mp3|wav|flac|aac)(\?.*)?$/,
                loader: 'url-loader',
                options: {
                    limit: 15000,
                    name: assetsPath('media/[name].[hash:7].[ext]')
                }
            },
            {
                test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
                // test: /\.(woff2?|eot|ttf|otf)(\?\S*)?$/,
                loader: 'url-loader',
                options: {
                    limit: 15000,
                    name: assetsPath('fonts/[name].[hash:7].[ext]')
                }
            }
            // {
            //     test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
            //     loader: 'url-loader?mimetype=application/font-woff',
            //     options: {
            //         limit: 10000,
            //         mimetype: 'application/font-woff',
            //         name: assetsPath('fonts/[name].[hash:7].[ext]')
            //     }
            // },
            // {
            //     test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
            //     loader: 'file-loader',
            //     options: {
            //         limit: 10000,
            //         name: assetsPath('fonts/[name].[hash:7].[ext]')
            //     }
            // }
        ]
    }
}
