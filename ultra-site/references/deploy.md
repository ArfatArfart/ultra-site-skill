# Deploy to GitHub Pages

## Vite

```js
export default defineConfig(({ command }) => ({
  base: command === 'build' ? '/<repo>/' : '/',
  build: { target: 'es2022', rollupOptions: { input: { main: 'index.html', notfound: '404.html' } } },
}));
```

Load runtime assets with `import.meta.env.BASE_URL + 'models/x.glb'`.

## Workflow `.github/workflows/deploy.yml`

```yaml
name: Deploy to GitHub Pages
on: { push: { branches: [main] }, workflow_dispatch: {} }
permissions: { contents: read, pages: write, id-token: write }
concurrency: { group: pages, cancel-in-progress: true }
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: npm ci --no-audit --no-fund
      - run: npm run build
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with: { path: dist }
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: { name: github-pages, url: ${{ steps.deployment.outputs.page_url }} }
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

Do not pass `--omit=optional` to `npm ci`: Vite 8 ships its bundler as platform specific optional packages.

## Repo and Pages from the terminal

If `gh` is not logged in but Git Credential Manager holds a GitHub login, feed it to `gh` for one
command at a time without printing it:

```bash
TOKEN=$(printf "protocol=https\nhost=github.com\n\n" | git credential fill | sed -n 's/^password=//p')
GH_TOKEN=$TOKEN gh repo create <repo> --public --source . --push
GH_TOKEN=$TOKEN gh api -X POST repos/<owner>/<repo>/pages -f build_type=workflow
GH_TOKEN=$TOKEN gh run watch $(GH_TOKEN=$TOKEN gh run list -L 1 --json databaseId -q '.[0].databaseId')
```

If the first run fails because Pages was enabled after the push, re-run with
`gh workflow run deploy.yml`. Verify the live URL loads and its console is clean.
