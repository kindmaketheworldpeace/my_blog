/*
* 全局js
* */
var app = window.app || {
    v: {},
    f: {
        encrypt: function (str, pubkey) {
            // Encrypt with the public key...
            var encrypt = new JSEncrypt();
            pubkey = (pubkey == undefined) ? $('body').data('pubkey') : pubkey;
            encrypt.setPublicKey(pubkey);
            return encrypt.encrypt(str);
        },
        decrypt: function (str, privatekey) {
            // Decrypt with the private key...
            var decrypt = new JSEncrypt();
            decrypt.setPrivateKey(privatekey);
            return decrypt.decrypt(str);
        }
    }


};