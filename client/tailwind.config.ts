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
        blueM: "rgba(175, 221, 229)",
        offWhite: "#F2F2F2",
        sun: "#FFD650",
        shade: "#9370DB",
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
      fontFamily: {
        avenir: ["var(--font-avenir)"],
      },
      fontWeight: {
        book: "400",
        roman: "500",
        heavy: "800",
      },
    },
  },
  plugins: [],
} satisfies Config;
