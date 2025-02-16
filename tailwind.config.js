export default {
  content: [
    "./index.html",
    "./**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        yale_blue: {
          DEFAULT: '#0d3b66',
          100: '#030c15',
          200: '#05182a',
          300: '#08243e',
          400: '#0b3053',
          500: '#0d3b66',
          600: '#1764ad',
          700: '#2e8ce4',
          800: '#74b2ed',
          900: '#b9d9f6'
        },
        lemon_chiffon: {
          DEFAULT: '#faf0ca',
          100: '#534408',
          200: '#a6880f',
          300: '#ebc326',
          400: '#f3da79',
          500: '#faf0ca',
          600: '#fbf4d6',
          700: '#fcf7e0',
          800: '#fdf9ea',
          900: '#fefcf5'
        },
        naples_yellow: {
          DEFAULT: '#f4d35e',
          100: '#3f3204',
          200: '#7e6509',
          300: '#bd970d',
          400: '#efc21e',
          500: '#f4d35e',
          600: '#f6dc7d',
          700: '#f8e59e',
          800: '#faedbe',
          900: '#fdf6df'
        },
        sandy_brown: {
          DEFAULT: '#ee964b',
          100: '#391d05',
          200: '#723b0b',
          300: '#ab5810',
          400: '#e47615',
          500: '#ee964b',
          600: '#f1ab6d',
          700: '#f5c092',
          800: '#f8d5b6',
          900: '#fceadb'
        },
        tomato: {
          DEFAULT: '#f95738',
          100: '#3b0b02',
          200: '#771704',
          300: '#b22206',
          400: '#ed2e07',
          500: '#f95738',
          600: '#fa7a61',
          700: '#fb9b88',
          800: '#fdbdb0',
          900: '#feded7'
        }
      }
    }
  },
  plugins: [],
}