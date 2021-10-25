import { register, init, getLocaleFromNavigator } from "svelte-i18n"

// Register translations
register("en", () => require("./translation/en.json"))


init({
    fallbackLocale: "en",
    initialLocale: getLocaleFromNavigator(),
})
