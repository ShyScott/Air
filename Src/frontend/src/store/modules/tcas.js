const tcas = {
  state: {
    selectedCourse: null,

    // the mode of page 'EditCourse'
    // 1 - Edit course name only
    // 2 - Import students only
    // 3 - Both (for creating a new course)
    editCourseMode: 3
  },
  mutations: {
    SET_SELECTED_COURSE: (state, selectedCourse) => {
      state.selectedCourse = selectedCourse
    },
    SET_EDIT_COURSE_MODE: (state, mode) => {
      state.editCourseMode = mode
    }
  },
  actions: {
    SetSelectedCourse ({ commit }, selectedCourse) {
      commit('SET_SELECTED_COURSE', selectedCourse)
    },
    SetEditCourseMode ({ commit }, mode) {
      commit('SET_EDIT_COURSE_MODE', mode)
    }
  }
}

export default tcas
