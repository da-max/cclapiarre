module.exports = {
    env: {
        browser: true,
        es2020: true
    },
    extends: [
        'plugin:vue/essential',
        'plugin:vue/recommended',
        'plugin:vue/strongly-recommended',
        'standard'
    ],
    parserOptions: {
        ecmaVersion: 12,
        sourceType: 'module'
    },
    plugins: [
        'vue'
    ],
    rules: {
        indent: ['error', 4]
    }
}
