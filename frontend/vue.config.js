const TerserPlugin = require('terser-webpack-plugin');

module.exports = {
    configureWebpack: {
        optimization: {
            minimizer: [new TerserPlugin({
                terserOptions: {
                    compress: {
                        warnings: false,
                        drop_debugger: true,
                        drop_console: true,
                        pure_funcs: ['console.log']
                    },
                },
                sourceMap: false,
                parallel: true,
            })]
        }
    },
    publicPath: process.env.VUE_APP_ROUTER_BASE_URL
}