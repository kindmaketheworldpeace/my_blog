/**
 * @file development env
 * @author ielgnaw <wuji0223@gmail.com>
 */
import merge from 'webpack-merge'
import prodEnv from './prod.env'

export default merge(prodEnv, {
    'process.env': {
        'NODE_ENV': JSON.stringify('development')
    },
    NODE_ENV: JSON.stringify('development'),
    BUILD_TARGET: JSON.stringify(process.env.BUILD_TARGET)
})
