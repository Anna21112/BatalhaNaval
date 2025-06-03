/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router/auto'
import { setupLayouts } from 'virtual:generated-layouts'
import { routes } from 'vue-router/auto-routes'
import Cadastro from '@/components/Cadastro.vue'
import Login from '@/components/Login.vue'
import BatalhaNaval from '@/components/BatalhaNaval.vue'
import NovaPartida from '@/components/novaPartida.vue'


// Add custom route to the auto-generated routes
routes.push({
  path: '/cadastro',
  name: 'cadastro',
  component: Cadastro,
}, {
  path: '/login',
  name: 'Login',
  component: Login,
},
{
  path: '/batalhanaval',
  name: 'batalhaNaval',
  component: BatalhaNaval,
},
{
  path: '/cadastro',
  name: 'Cadastro',
  component: Cadastro },

{
  path: '/login',
  name: 'login',
  component: Login },

{
  path: '/batalhanaval',
  name: 'batalhanaval',
  component: BatalhaNaval },
{
  path: '/novapartida',
  name: 'novapartida',
  component: NovaPartida } )

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: setupLayouts(routes),
})

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (!localStorage.getItem('vuetify:dynamic-reload')) {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    } else {
      console.error('Dynamic import error, reloading page did not fix it', err)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router
