import svelte from 'rollup-plugin-svelte';
import resolve from '@rollup/plugin-node-resolve';
import css from 'rollup-plugin-css-only';
import del from 'rollup-plugin-delete';
import { copy } from '@web/rollup-plugin-copy';

export default {
    input: [
        'frontend/main.js',
        'frontend/api.js'
    ],
    output: {
        dir: 'backend/static',
        format: 'es',
        entryFileNames: 'js/[name].js',
        chunkFileNames: 'js/[name].js',
        manualChunks: {
            svelte: ['svelte', 'svelte/store'],
            router: ['svelte-spa-router']
        }
    },
    plugins: [
        svelte({
            onwarn: (warning, handler) => {
                if (warning.code.startsWith('a11y-')) {
                    return;
                }
                handler(warning);
            }
        }),
        resolve(),
        css({
            output: 'css/bundle.css'
        }),
        del({
            targets: ['backend/static/css', 'backend/static/js']
        }),
        copy({
            patterns: '**/*',
            rootDir: './frontend/static'
        })
    ]
};
