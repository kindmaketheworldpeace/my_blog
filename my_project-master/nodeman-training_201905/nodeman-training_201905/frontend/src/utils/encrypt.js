
/**
 *  获取元素相对于页面的高度
 *  @param node {NodeElement} 指定的DOM元素
 */
import Vue from 'vue'
import JsEncrypt from 'jsencrypt'

export function encrypt (str) {
    // Encrypt with the public key...
    debugger
    var encrypt = new JsEncrypt()
    encrypt.setPublicKey(window.pubkey)
    return encrypt.encrypt(str)
}

Vue.prototype.$encrypt = encrypt
