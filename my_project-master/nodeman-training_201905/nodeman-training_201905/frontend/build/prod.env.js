/**
 * @file production env
 * @author ielgnaw <wuji0223@gmail.com>
 */

let result = {}

if (process.env.NODE_ENV !== 'development') {
    const NODE_ENV = JSON.stringify('production')

    // 打包的环境，staging test master
    const BUILD_ENV = process.argv[2]

    result = {
        'process.env': {
            'NODE_ENV': NODE_ENV
        },
        NODE_ENV: NODE_ENV,
        BUILD_TARGET: JSON.stringify(process.env.BUILD_TARGET)
    }
}

export default result
