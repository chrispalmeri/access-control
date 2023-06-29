module.exports = {
    root: true,
    env: {
        browser: true,
        es2021: true
    },
    extends: [
        'eslint:recommended',
        'plugin:svelte/recommended',
        'standard'
    ],
    parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module'
    },
    ignorePatterns: [
        'backend/static/*'
    ],
    rules: {
        'svelte/valid-compile': 'off',
        semi: ['error', 'always'],
        indent: ['error', 4],
        'space-before-function-paren': ['error', {
            anonymous: 'always',
            named: 'never',
            asyncArrow: 'always'
        }],
        'object-shorthand': ['error', 'consistent']
    }
};
