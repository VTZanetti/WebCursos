import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import CourseDetailView from '../views/CourseDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
      meta: {
        title: 'Dashboard - WebCurso'
      }
    },
    {
      path: '/curso/:id',
      name: 'course-detail',
      component: CourseDetailView,
      meta: {
        title: 'Detalhes do Curso - WebCurso'
      }
    },
    // Redirect para dashboard se a rota não existir
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ]
})

// Guard para atualizar o título da página
router.beforeEach((to, from, next) => {
  document.title = to.meta?.title || 'WebCurso'
  next()
})

export default router