import { asyncRouterMap, constantRouterMap, studentRoutes, teacherRoutes } from '@/config/router.config'

const permission = {
  state: {
    routers: constantRouterMap,
    addRouters: []
  },
  mutations: {
    SET_ROUTERS: (state, routers) => {
      state.addRouters = routers
      state.routers = constantRouterMap.concat(routers)
    }
  },
  actions: {
    GenerateRoutes ({ commit }, isTeacher) {
      return new Promise(resolve => {
        const routes = asyncRouterMap
        routes[0].children = isTeacher ? teacherRoutes : studentRoutes
        commit('SET_ROUTERS', routes)
        resolve()
      })
    }
  }
}

export default permission
