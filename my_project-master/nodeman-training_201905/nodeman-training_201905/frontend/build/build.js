/**
 * @file build
 * @author ielgnaw <wuji0223@gmail.com>
 */

import {join} from 'path'
import ora from 'ora'
import chalk from 'chalk'
import webpack from 'webpack'
import rm from 'rimraf'
import shell from 'shelljs'

import checkVer from './check-versions'
import config from './config'
import webpackConf from './webpack.prod.conf'

process.env.NODE_ENV = 'production'

checkVer()

// 打包的目标，cd ci all
// const BUILD_TARGET = process.argv[3]

// 打包的环境，staging test master
const BUILD_ENV = process.argv[2]

const spinner = ora(`building for ${chalk.green(BUILD_ENV)}`)
spinner.start()

// console.log(1, join(config.build.assetsRoot, config.build.assetsSubDirectory))
// console.log(2, join(config.build.assetsRoot, config.build.assetsSubDirectory, '..'))
// console.log(3, join(config.build.assetsRoot, BUILD_TARGET))

rm(join(config.build.assetsRoot, config.build.assetsSubDirectory), e => {
    if (e) {
        throw e
    }
    webpack(webpackConf, (err, stats) => {
        spinner.stop()
        if (err) {
            throw err
        }
        process.stdout.write(stats.toString({
            colors: true,
            modules: false,
            children: false,
            chunks: false,
            chunkModules: false
        }) + '\n\n')

        if (stats.hasErrors()) {
            console.log(chalk.red('  Build failed with errors.\n'))
            process.exit(1)
        }

        console.log(chalk.cyan('  Build complete.\n'))
        console.log(chalk.yellow(
            '  Tip: built files are meant to be served over an HTTP server.\n'
            + '  Opening index.html over file:// won\'t work.\n'
        ))
    })
})
