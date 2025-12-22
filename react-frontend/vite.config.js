import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'node:fs'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    {
      name: 'debug-file-structure',
      configResolved(config) {
        console.log('DEBUG: Vite Root:', config.root);
        try {
          console.log('DEBUG: Root Directory Contents:', fs.readdirSync(config.root));
          if (fs.existsSync(config.root + '/src')) {
             console.log('DEBUG: src Directory Contents:', fs.readdirSync(config.root + '/src'));
          } else {
             console.log('DEBUG: src directory NOT FOUND at ' + config.root + '/src');
          }
        } catch (e) {
          console.error('DEBUG: Error reading directory', e);
        }
      }
    }
  ],
  base: './', // Use relative paths for assets
})
