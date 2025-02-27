import type { Config } from "tailwindcss";

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        gray: "#C3C3C3",
        orange: "#FF5000",
        green: "#009E92",
        blue: "#00A4CC",
        magenta: "#D70074",
        yellow: "#FFD650",
        "yellow-pale": "#fff3ed",
        // Dark mode
        dark: {
          gray: "#181a1b",
          banner: "#3e1500",
        },
        // Variables
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
      // Fonts
      fontFamily: {
        avenir: ["var(--font-avenir)"],
      },
      fontWeight: {
        book: "400",
        roman: "500",
      },
    },
  },
  plugins: [],
} satisfies Config;
