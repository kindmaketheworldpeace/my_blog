/**
 * @file webpack dll conf
 * @author ielgnaw <wuji0223@gmail.com>
 */

import path from 'path'
import webpack from 'webpack'

export default {
    entry: {
        vendor: ['vue/dist/vue.esm.js', 'vue-router', 'vuex', 'axios'],
    },
    output: {
        path: path.join(__dirname, '../dist/dll/js'),
        filename: '[name].dll.js',
        library: '[name]_library'       // vendor.dll.js 中暴露出的全局变量名
    },
    plugins: [
        new webpack.DllPlugin({
            path: path.join(__dirname, '..', '[name]-manifest.json'),
            name: '[name]_library',
            context: path.resolve(__dirname, '..')
        }),
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                warnings: false
            }
        })
    ]
}
