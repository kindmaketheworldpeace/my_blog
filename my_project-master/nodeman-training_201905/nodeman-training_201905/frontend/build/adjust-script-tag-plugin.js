/**
 * @file 构建后的 html 中 script 和 link 中的 /ci/static/js/... 替换成 /static/js/...
 * @author ielgnaw <wuji0223@gmail.com>
 */

import cheerio from 'cheerio';

export default class AdjustScriptTagPlugin {
    constructor(props) {}
    apply(compiler) {
        compiler.plugin('compilation', compilation => {
            compilation.plugin('html-webpack-plugin-after-html-processing', (htmlPluginData, callback) => {
                const $ = cheerio.load(htmlPluginData.html);

                const scriptList = $('script')
                scriptList.each((index, script) => {
                    script.attribs.src = script.attribs.src.replace(/^\/(ci|cd)\/static\/js/, '/static/js')
                })

                const linkList = $('link')
                linkList.each((index, link) => {
                    link.attribs.href = link.attribs.href.replace(/^\/(ci|cd)\/static\/css/, '/static/css')
                })

                htmlPluginData.html = $.html({
                    decodeEntities: false
                });

                callback(null, htmlPluginData);
            });
        });
    }
};
