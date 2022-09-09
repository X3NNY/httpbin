module.exports = {
    devServer: {
        disableHostCheck: true,
        open: true,
        host: '0.0.0.0',
        port: 8000,
        https: false,
        proxy: { //配置跨域
            '/': {
                target: 'http://api.httpbin.ctfer.vip/', //填写你们真实的后台接口
                ws: true,
                changOrigin: true, //允许跨域
                pathRewrite: {
                    '^/': '' //请求的时候使用这个api就可以
                }
            }

        }
    },
    assetsDir: "static",
    productionSourceMap: false
}