const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer')
const BundleTracker = require('webpack-bundle-tracker')

module.exports = {
    publicPath: 'http://localhost:8000/static/',
    outputDir: 'dist/',

    runtimeCompiler: true,
    chainWebpack: (config) => {
        config.optimization.splitChunks(false)
        config
            .plugin('BundleTracker')
            .use(BundleTracker, [{ filename: 'webpack-stats.json' }])
        config.resolve.alias.set('__STATIC__', 'static')
        config.devServer
            .public('http://0.0.0.0:8080')
            .host('0.0.0.0')
            .port(8080)
            .hotOnly(true)
            .watchOptions({ poll: 1000 })
            .https(false)
            .headers({ 'Access-Control-Allow-Origin': ['*'] })

        // Graphql Loader
        config.module
            .rule('graphql')
            .test('/.(graphql|gql)$/')
            .use('graphql-tag/loader')
            .loader('graphql-tag/loader')
            .end()
    },

    pluginOptions: {
        apollo: {
            lintGQL: true
        }
    },

    configureWebpack: {
        plugins: [new BundleAnalyzerPlugin()]
    }
}
