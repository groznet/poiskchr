module.exports = {
    content: [
        "./layouts/**/*.html",
        "./content/**/*.md",
        "./content/**/*.html",
        "./assets/**/*.js"
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ["Inter", "ui-sans-serif", "system-ui", "-apple-system", "Segoe UI", "Roboto", "Ubuntu", "Cantarell", "Noto Sans", "Helvetica Neue", "Arial"],
            },
            colors: {
                testColor: "#ff00ff",
                primary: {
                    DEFAULT: "#1E5AB8",
                },
                secondary: {
                    lightBlue: "#4A90E2",
                    creamBeige: "#F5F1E8",
                    golden: "#D4A574",
                },
                neutrals: {
                    white: "#FFFFFF",
                    lightGray: "#F8F9FA",
                    textGray: "#333333",
                    borderGray: "#E0E0E0",
                },
            },
            boxShadow: {
                vintage: "inset 0 0 0 1px rgba(0,0,0,0.05), 0 10px 25px rgba(0,0,0,0.18)",
                insetPaper: "inset 0 1px 0 rgba(255,255,255,0.6), inset 0 -1px 0 rgba(0,0,0,0.06)",
            },
            backgroundImage: {
                blueTexture:
                    "linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0) 40%), radial-gradient(140% 100% at 10% 0%, #2A6ED5 0%, #1E5AB8 55%, #1A4C97 100%)",
            },
        },
    },
    plugins: [
        require("@tailwindcss/typography")
    ],
    corePlugins: {
        container: false,
    },
}