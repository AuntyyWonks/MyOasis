/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Composables
import { createVuetify } from 'vuetify'
// Styles
import '@mdi/font/css/materialdesignicons.css'

import 'vuetify/styles'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          'primary': '#2196F3', // Azure Blue
          'secondary': '#689F38', // Olive Green
          'accent': '#F5F5F5', // Gray-White
          'azure-blue': '#2196F3',
          'olive-green': '#689F38',
          'gray-white': '#F5F5F5',
          'surface': '#FFFFFF',
          'background': '#F8F9FA',
        },
      },
    },
  },
})
