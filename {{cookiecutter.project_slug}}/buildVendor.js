const gzipPlugin = require('@luncheon/esbuild-plugin-gzip');
const esbuild = require('esbuild');

const modulePath = process.env.NODE_PATH || 'node_modules';
const nodePaths = [modulePath];

process.env.NODE_ENV = 'production';

const target = [
  'es2020', 'chrome58', 'firefox57', 'safari11',
];
const outdir = './{{cookiecutter.project_slug}}/admin/static/vendor';

esbuild
  .build({
    entryPoints: [
      './vendor/vendor.js',
    ],
    bundle: true,
    minify: true,
    sourcemap: true,
    plugins: [gzipPlugin({
      uncompressed: false,
      gzip: true,
      brotli: false,
    })],
    loader: {
      '.png': 'base64',
      '.svg': 'base64',
      '.woff': 'dataurl',
      '.woff2': 'dataurl',
      '.eot': 'dataurl',
      '.ttf': 'dataurl',
    },
    format: 'esm',
    write: false,
    outdir,
    target,
    nodePaths,
  });

esbuild
  .build({
    entryPoints: [
      'es-module-shims',
    ],
    bundle: true,
    minify: true,
    sourcemap: true,
    format: 'iife',
    plugins: [gzipPlugin({
      uncompressed: false,
      gzip: true,
      brotli: false,
    })],
    outdir,
    write: false,
    target,
    nodePaths,
  });
