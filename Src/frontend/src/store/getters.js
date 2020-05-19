const getters = {
  device: state => state.app.device,
  theme: state => state.app.theme,
  color: state => state.app.color,
  token: state => state.user.token,
  avatar: state => (state.user.avatar) ? state.user.avatar.small : null,
  avatarMedium: state => (state.user.avatar) ? state.user.avatar.medium : null,
  nickname: state => state.user.name,
  addRouters: state => state.permission.addRouters,
  multiTab: state => state.app.multiTab,
  lang: state => state.i18n.lang,
  isTeacher: state => state.user.isTeacher,
  userId: state => state.user.id,
  selectedCourse: state => state.tcas.selectedCourse,
  editCourseMode: state => state.tcas.editCourseMode
}

export default getters
