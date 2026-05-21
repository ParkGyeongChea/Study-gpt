/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
  extend: {
    keyframes: {
      fadeIn: {
        "0%": {
          opacity: "0",
          transform: "translateY(25px)"
        },
        "100%": {
          opacity: "1",
          transform: "translateY(0px)"
        }
      }
    },
    animation: {
      messageFade: "fadeIn 0.4s ease",
      pageFade: "fadeIn 0.8s ease"
    }
  },
},
  plugins: [
    require("@tailwindcss/typography"),
  ],
}