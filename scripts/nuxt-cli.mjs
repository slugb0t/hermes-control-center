#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const webRoot = resolve(repoRoot, 'apps/web');
const requireFromWeb = createRequire(resolve(webRoot, 'package.json'));
const nuxtPackageJson = requireFromWeb.resolve('nuxt/package.json');
const nuxtBin = resolve(dirname(nuxtPackageJson), 'bin/nuxt.mjs');
const args = process.argv.slice(2);

const result = spawnSync(process.execPath, [nuxtBin, ...args], {
  cwd: webRoot,
  env: process.env,
  stdio: 'inherit',
  shell: false,
});

if (result.error) {
  console.error(result.error);
  process.exit(1);
}

process.exit(result.status ?? 1);
